import os
import time

def write_to_file(sents, end):
    with open('file.txt', 'w') as f:
        for s in sents:
            f.write(s.strip())
            f.write(f'{end} \n')
        f.close()


def read_predictions(res):
    with open('file.txt.out', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'Text=' not in line:
                continue
            aux_line = line[1:-1].split()
            aux_dict = {}
            for l in aux_line:
                aux = l.split('=')
                if aux[0] != 'NamedEntityTag' and aux[0] != 'Text':
                    continue
                aux_dict[aux[0]] = aux[1]
            res.append(aux_dict)


    return res



def make_prediction(sents, lang='spanish', path = "/media/windows/Tesis/NER/Stanford_NLP/stanford-corenlp-4.3.1/*",
                    end='', batch_size=100):
    res = []
    for b in range(len(sents)//batch_size + 1):
        if len(sents[b*batch_size:(b+1)*batch_size]) == 0:
            print('continue due to size cero')
            continue
        write_to_file(sents[b*batch_size:(b+1)*batch_size], end)
        os.system('pwd')
        print(len(sents[b*batch_size:(b+1)*batch_size]))
        # os.system(f'export CLASSPATH=$CLASSPATH:{path} && java -Xmx5g edu.stanford.nlp.pipeline.StanfordCoreNLP -props {lang} -file file.txt')
        time.sleep(2)
        res =  read_predictions(res)
    return res