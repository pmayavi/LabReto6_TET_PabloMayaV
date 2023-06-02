from mrjob.job import MRJob
from mrjob.step import MRStep

# Reto 3 - e

class PeorCalificacion(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            rating = filing[2]
            fecha = filing[4]
            yield fecha, float(rating)

    def reducer(self, key, values):
        ratingTotal = 0
        count = 0

        for rating in values:
            ratingTotal += rating
            count += 1

        ratingProm = ratingTotal / count

        yield None, (ratingProm, key)

    def findMin(self, _, values):
        menorProm = float('inf')
        menorFecha = None

        for ratingProm, fecha in values:
            if ratingProm < menorProm:
                menorProm = ratingProm
                menorFecha = fecha

        yield menorFecha, menorProm

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.findMin)
        ]

if __name__ == '__main__':
    PeorCalificacion.run()