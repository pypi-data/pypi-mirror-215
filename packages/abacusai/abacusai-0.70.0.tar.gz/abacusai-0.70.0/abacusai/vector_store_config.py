from .api_class import VectorStoreConfig
from .return_class import AbstractApiClass


class VectorStoreConfig(AbstractApiClass):
    """
        A config for vector store creation.

        Args:
            client (ApiClient): An authenticated API Client instance
            chunkSize (int): The size of chunks for vector store.
            chunkOverlapFraction (float): The fraction of overlap between two consecutive chunks.
    """

    def __init__(self, client, chunkSize=None, chunkOverlapFraction=None):
        super().__init__(client, None)
        self.chunk_size = chunkSize
        self.chunk_overlap_fraction = chunkOverlapFraction

    def __repr__(self):
        return f"VectorStoreConfig(chunk_size={repr(self.chunk_size)},\n  chunk_overlap_fraction={repr(self.chunk_overlap_fraction)})"

    def to_dict(self):
        """
        Get a dict representation of the parameters in this class

        Returns:
            dict: The dict value representation of the class parameters
        """
        return {'chunk_size': self.chunk_size, 'chunk_overlap_fraction': self.chunk_overlap_fraction}
