import os

def write_to_file(sents, end):
    list = []
    for i in range(len(sents)):
        list.append(f'temp/file_{i}.txt')
        with open(f'temp/file_{i}.txt', 'w') as f:
            f.write(sents[i])
            f.write(f'{end} \n')
            f.close()

    with open('list.txt', 'w') as f:
        for w in list:
            f.write(w)
            f.write('\n')
        f.close()


def read_predictions(res, n_files, cur_num=0):
    for i in range(n_files):
        with open(f'temp/file_{i}.txt.out', 'r') as f:
            lines = f.readlines()
            inter = False
            for line in lines:
                if "Extracted the following NER entity mentions:" in line:
                    inter = True
                    continue
                if not inter:
                    continue
                if len(line) <= 1:
                    inter = False
                    continue
                aux = {}
                aux['Text'] = line.split('\t')[0]
                if len(line.split('\t')) > 1:
                    aux['TAG'] = line.split('\t')[-1]
                aux['File'] = i + cur_num
                res.append(aux)
            f.close()


    return res


def fix_endl(res):
    ret = []
    for ind in range(len(res)):
        if len(res[ind]) >= 3:
            ret.append(res[ind].copy())
        else:
            aux = res[ind]
            while len(aux) < 3:
                aux = res[ind+1]
                for k in res[ind+1]:
                    if k == 'Text':
                        continue
                    aux[k] = res[ind+1][k]
                aux['Text'] = aux['Text'] + " " + res[ind+1]['Text']
                ind +=1
            ret.append(aux.copy())

    return ret



def make_prediction(sents, lang='spanish', path = "/media/NAS/Tesis/NER/Stanford_NLP/stanford-corenlp-4.3.1/*",
                    end='', batch_size=500):
    res = []
    cur = 0
    for b in range(len(sents)//batch_size + 1):
        print(len(sents[b*batch_size:(b+1)*batch_size]))
        if len(sents[b*batch_size:(b+1)*batch_size]) == 0:
            print('continue due to size cero')
            continue
        write_to_file(sents[b*batch_size:(b+1)*batch_size], end)
        cmd = f'export CLASSPATH=$CLASSPATH:{path} && java -Xmx5g edu.stanford.nlp.pipeline.StanfordCoreNLP -props {lang} -filelist list.txt'
        # for i in range(len(sents[b*batch_size:(b+1)*batch_size])):
        #     cmd = cmd + f'-file temp/file_{i}.txt '
        print(cmd)
        os.system(cmd)
        os.system('mv file_* temp/')
        res =  read_predictions(res, len(sents[b*batch_size:(b+1)*batch_size]), cur)
        cur+=batch_size
    return fix_endl(res)