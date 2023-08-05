class jaccard:
    def calculate(dokumen_a, dokumen_b):
        """
        Menghitung similaritas Jaccard antara dua teks input.
        
        Referensi:
        https://en.wikipedia.org/wiki/Jaccard_index
        
        Rumus : 
        Jaccard Similarity = (Jumlah Intersection) / (Jumlah Union)
        
        Args:
            dokumen_a (str): Teks pertama.
            dokumen_b (str): Teks kedua.
        
        Returns:
            float: Nilai similaritas Jaccard antara dua teks.
        """
        set1 = set(dokumen_a)
        set2 = set(dokumen_b)

        # Menghitung jumlah irisan dan jumlah union dari kedua set
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        # Menghitung similaritas Jaccard dan mengembalikan nilainya
        similarity = float(intersection) / float(union) if union != 0 else 0.0
        
        return similarity