from mrjob.job import MRJob
from datetime import datetime

class listaAcciones(MRJob):

    def mapper(self, _, line):
        for w in line.split():
            filing = w.split(',')
            comp = filing[0]
            precio = float(filing[1])
            fechStr = datetime.strptime(filing[2].strip(), '%Y-%m-%d').strftime('%Y-%m-%d')
            yield comp, (fechStr, precio)

    def reducer(self, comp, values):
        sorted_values = sorted(values, key=lambda x: x[0])
        precioAnt = None
        inc = True

        for _, precio in sorted_values:
            if precioAnt is not None and precio < precioAnt:
                inc = False
                break

            precioAnt = precio

        if inc:
            yield comp, 'Sube o se mantiene estable'
        else:
            yield comp, 'Baja o no es estable'

if __name__ == '__main__':
    listaAcciones.run()