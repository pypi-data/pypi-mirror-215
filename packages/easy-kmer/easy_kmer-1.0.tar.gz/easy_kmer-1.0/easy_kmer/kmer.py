class Kmer:
    def __init__(self, sequence, k):
        self.sequence = sequence
        self.k = k

    def get_kmers(self):
        kmers = []
        for i in range(len(self.sequence) - self.k + 1):
            kmer = self.sequence[i:i + self.k]
            kmers.append(kmer)
        return kmers

    def count_kmers(self):
        kmers = self.get_kmers()
        kmer_counts = {}
        for kmer in kmers:
            if kmer in kmer_counts:
                kmer_counts[kmer] += 1
            else:
                kmer_counts[kmer] = 1
        return kmer_counts

    def most_frequent_kmers(self, top_n=None):
        kmer_counts = self.count_kmers()
        sorted_kmers = sorted(kmer_counts.items(), key=lambda x: x[1], reverse=True)
        if top_n is not None:
            sorted_kmers = sorted_kmers[:top_n]
        return sorted_kmers

    def reverse_complement(self):
        complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
        reverse = self.sequence[::-1]
        reverse_complement = "".join(complement.get(base, base) for base in reverse)
        return reverse_complement
