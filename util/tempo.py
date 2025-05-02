from datetime import timedelta


def formatar_tempo(segundos):
    td = timedelta(seconds=segundos)
    tempo_str = str(td)
    if '.' in tempo_str:
        tempo_str = tempo_str.split('.')[0] + ',' + tempo_str.split('.')[1][:3]
    else:
        tempo_str += ',000'
    return tempo_str.rjust(12, '0')