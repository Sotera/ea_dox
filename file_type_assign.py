from itertools import groupby
def is_sql(line):
    key = " ".join(line.split()[:2])
    if key in ["INSERT INTO", "CREATE TABLE"]:
        return True
    return False

def csv_potential(line, char):
    return (len(line.split(char)), 1)


def move_to_folder(file):
    #return types:
    #0 - sql
    #1 - csv/tsv
    #2 - hash
    #3 - space delimited/ambiguous
    #4 - unstructured/dox
    f0 = open(file, "r")
    n_lines = 0
    delim = [",", ":", "\t", " "]
    d_csv = {}
    for d in delim:
        d_csv[d] = []
    try:
        for line in f0:
            if is_sql(line):
                return 0 #0 type = sql
            for d in delim:
                d_csv[d].append(csv_potential(line, d))
            n_lines += 1
            if n_lines == 150:
                break


        for k, v in d_csv.iteritems():
            m_v = list(max(groupby(v)))[0]
            if float(len(filter(lambda x: x==m_v, v)))/len(v) > .8:
                if k == "," or k == "\t":
                    return 1
                elif k == ":" and m_v == 2:
                    return 2
                elif k == ":":
                    return 1
                elif k == " ":
                    return 3

        return 4
    except:
        print("File:", file)
        print("Unexpected error:", sys.exc_info()[0])
        print("Line:", line)
        return -1