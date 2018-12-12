import multiprocessing
from threaded_crawler import threaded_crawler


def process_link_crawler(args, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    print('Starting {} processes'.format(num_cpus))
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(
            target=threaded_crawler, args=[args], kwargs=kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()
