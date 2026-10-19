def fcfs(proses):

    waktu = 0

    hasil = []

    for nama, burst in proses:

        selesai = waktu + burst

        tat = selesai

        wt = tat - burst

        hasil.append((nama, burst, waktu, selesai, wt, tat))

        waktu = selesai

    return hasil

def sjf(proses):

    urut = sorted(proses, key=lambda p: p[1])

    return fcfs(urut)

if __name__ == "__main__":

    dataset = {

        "D1": [("A", 7), ("B", 4), ("C", 1), ("D", 4)],

        "D2": [("A", 10), ("B", 10), ("C", 10)],

        "D3": [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)],

    }

    for nama, proses in dataset.items():

        print(nama, "FCFS:", fcfs(proses))

        print(nama, "SJF:", sjf(proses))
