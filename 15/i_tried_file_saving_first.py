samples_per_file = 10000

def load_cur_idx(data_dir):
    data_files = os.listdir(data_dir)
    return len(data_files) * samples_per_file

def find_distance(cur_page):
    once = False
    if cur_page:
        val = cur_page[-1]
        dist = 0
        rest_of_cur_page = cur_page[:-1]
        for elem in rest_of_cur_page[::-1]:
            dist += 1
            if elem == val:
                return dist
    data_files = sorted(os.listdir("data"))
    for data_file in data_files[::-1]:
        lines = []
        with open("data/{}".format(data_file),"r") as f:
            for line in f:
                lines.append(int(line))
        if not cur_page and not once:
            val = lines.pop(-1)
            dist = 0
            once = True
        for elem in lines[::-1]:
            dist += 1
            if elem == val:
                return dist
    return -1

def last_val_from_file():
    data_files = sorted(os.listdir("data"))
    data_file = data_files[-1]
    lines = []
    with open("data/{}".format(data_file),"r") as f:
        for line in f:
            lines.append(int(line))
    return lines[-1]

def save_progress(first_samples, sample_no):
    if not os.path.isdir("data"):
        logging.debug("creating data dir")
        os.mkdir("data")
    cur_idx = load_cur_idx("data")
    logging.info("loaded cur_idx: %d" % cur_idx)
    if cur_idx == 0:
        cur_page = first_samples
        cur_idx = len(first_samples)
        last_val = cur_page[-1]
    else:
        cur_page = []
        last_val = last_val_from_file()
        
    # cur_page initialized with current buffer
    # cur_idx initialized
    while cur_idx < sample_no:
        dist = find_distance(cur_page)
        if dist == -1:
            logging.debug("no distance, appending 0")
            last_val = 0
        else:
            logging.debug("appending distance: %d" % dist)
            last_val = dist
        cur_page.append(last_val)
        cur_idx += 1
        if len(cur_page)  == samples_per_file:
            logging.info("%d / %d " % (cur_idx, sample_no))
            filename = "data/data{:010d}".format((cur_idx // samples_per_file) - 1)
            logging.info("saving file %s" % filename)
            with open(filename, "w") as f:
                for sample in cur_page:
                    f.write("%s\n" % sample)
            cur_page = []
            assert(cur_idx % samples_per_file == 0)
    return last_val