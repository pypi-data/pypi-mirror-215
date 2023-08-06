from enum import StrEnum
import functools
import random
from functools import lru_cache
from typing import Callable, Mapping, Optional, Sequence, Tuple, Union
from torch.utils.data import Dataset as TorchDataset

import numpy as np
import torch
import torch.nn.functional as F
from pytorch_lightning import seed_everything
from sklearn.cluster import KMeans
from torch.utils.data import Dataset as TorchDataset
from torch_geometric.nn import fps

from latentis.utils.openfaiss import FaissIndex


class AnchorChoice(StrEnum):
    UNIFORM = "uniform"
    FPS = "fps"
    KMEANS = "kmeans"


class LatentSpace(TorchDataset):
    def __init__(
        self,
        encoding_type: str,
        encoder: str,
        num_classes: int,
        keys: Sequence[str] = None,
        vectors: torch.Tensor = None,
        labels: torch.Tensor = None,
    ):
        self.encoding_type: str = encoding_type
        assert ((keys is None) + (vectors is None)) % 2 == 0
        assert keys is None or len(keys) == vectors.size(0)

        self.key2index: Mapping[str, int] = keys if keys is None else {key: index for index, key in enumerate(keys)}
        self.index2key: Mapping[int, str] = None if keys is None else {index: key for index, key in enumerate(keys)}

        self.vectors: torch.Tensor = vectors
        self.encoder: str = encoder
        self.num_classes: int = num_classes
        self.labels: torch.Tensor = labels

    @property
    def shape(self) -> int:
        return self.vectors.shape

    def __repr__(self) -> str:
        return f"LatentSpace(encoding_type={self.encoding_type}, encoder={self.encoder}, shape={self.shape})"

    # @lru_cache
    # def to_faiss(self, normalize: bool, keys: Sequence[str]) -> FaissIndex:
    #     index: FaissIndex = FaissIndex(d=self.vectors.size(1))
    #     index.add_vectors(
    #         embeddings=list(zip(keys, self.vectors.cpu().numpy())),
    #         normalize=normalize,
    #     )
    #     return index

    def to_relative(
        self,
        projection_name: str,
        projection_func: Callable[[torch.Tensor], Tuple[torch.Tensor, torch.Tensor]],
        anchor_choice: str = None,
        seed: int = None,
        anchors: Optional[Mapping[str, torch.Tensor]] = None,
        num_anchors: int = None,
    ) -> "RelativeSpace":
        assert self.encoding_type != "relative"  # TODO: for now
        assert (anchors is None) or (num_anchors is None)

        anchors = (
            self.get_anchors(anchor_choice=anchor_choice, seed=seed, num_anchors=num_anchors)
            if anchors is None
            else anchors
        )

        anchor_keys, anchor_latents = list(zip(*anchors.items()))
        anchor_latents = torch.stack(anchor_latents, dim=0).cpu()

        relative_vectors = projection_func(
            anchors=anchor_latents,
            points=self.vectors,
        )

        return RelativeSpace(
            keys=self.key2index.keys(),
            vectors=relative_vectors,
            labels=self.labels,
            encoder=self.encoder,
            anchors=anchor_keys,
            projection=projection_name,
            num_classes=self.num_classes,
        )

    @lru_cache()
    def get_anchors(self, anchor_choice: AnchorChoice, seed: int, num_anchors: int) -> Mapping[str, torch.Tensor]:
        # Select anchors
        seed_everything(seed)

        if anchor_choice == AnchorChoice.UNIFORM:
            limit: int = len(self.key2index.keys()) if anchor_choice == "uniform" else int(anchor_choice[4:])
            anchor_set: Sequence[str] = random.sample(list(self.key2index.keys())[:limit], num_anchors)
            
        elif anchor_choice == AnchorChoice.FPS:
            anchor_fps = F.normalize(self.vectors, p=2, dim=-1)
            anchor_fps = fps(anchor_fps, random_start=True, ratio=num_anchors / len(self.key2index.keys()))
            anchor_set: Sequence[str] = [self.index2key[sample_index] for sample_index in anchor_fps.cpu().tolist()]

        elif anchor_choice == AnchorChoice.KMEANS:
            vectors = F.normalize(self.vectors)
            clustered = KMeans(n_clusters=num_anchors, random_state=seed).fit_predict(vectors.cpu().numpy())

            all_targets = sorted(set(clustered))
            cluster2embeddings = {target: vectors[clustered == target] for target in all_targets}
            cluster2centroid = {
                cluster: centroid.mean(dim=0).cpu().numpy() for cluster, centroid in cluster2embeddings.items()
            }
            centroids = np.array(list(cluster2centroid.values()), dtype="float32")

            index: FaissIndex = FaissIndex(d=vectors.shape[1])
            index.add_vectors(list(zip(self.key2index.keys(), vectors.cpu().numpy())), normalize=False)
            centroids = index.search_by_vectors(query_vectors=centroids, k_most_similar=1, normalize=True)

            anchor_set = [list(sample2score.keys())[0] for sample2score in centroids]
        else:
            assert NotImplementedError

        return {anchor_key: self.vectors[self.key2index[anchor_key]] for anchor_key in sorted(anchor_set)}

    def __getitem__(self, index: int) -> Mapping[str, torch.Tensor]:
        return {"x": self.vectors[index], "y": self.labels[index]}

    def __len__(self) -> int:
        return self.vectors.size(0)


class RelativeSpace(LatentSpace):
    def __init__(
        self,
        keys: Sequence[str],
        vectors: torch.Tensor,
        labels: torch.Tensor,
        anchors: Sequence[str],
        projection: str,
        num_classes: int,
        encoder: str = None,
    ):
        super().__init__(
            encoding_type="relative",
            keys=keys,
            num_classes=num_classes,
            vectors=vectors,
            labels=labels,
            encoder=encoder,
        )
        self.anchors: Sequence[str] = anchors
        self.projection: str = projection

    def __repr__(self) -> str:
        return f"LatentSpace(encoding_type={self.encoding_type}, projection={self.projection}, encoder={self.encoder}, shape={self.shape})"
