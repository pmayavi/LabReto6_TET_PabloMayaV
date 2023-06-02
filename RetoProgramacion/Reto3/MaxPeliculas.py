from mrjob.job import MRJob
from mrjob.step import MRStep

# Reto 3 - b

class MaxPeliculas(MRJob):
    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            fecha= filing[4]
            yield fecha, 1

    def reducer(self, key, values):
        vistas = sum(values)
        yield None, (vistas, key)

    def findMax(self, _, vistasFechas):
        vistasMax = 0
        fechaMax = None
        for vistas, fecha in vistasFechas:
            if vistas > vistasMax:
                vistasMax = vistas
                fechaMax = fecha
        yield fechaMax, vistasMax

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.findMax)
        ]

if __name__ == '__main__':
    MaxPeliculas.run()