import asyncio
from time import perf_counter
from typing import List
from ...genetics.gene import Gene
from ...genetics.allele import Allele
from ...utils.generators.char_generator import random_chars
from ...config import get_logger

log = get_logger(__name__)


# --------------------------------------------------------------------------- #
def least_common_divisor(num):
    for i in range(1, num + 1):
        if num % i == 0:
            for divisor in range(2, i + 1):
                if (i % divisor == 0) and (num % divisor == 0):
                    return divisor


# --------------------------------------------------------------------------- #
def population_generator(n: int = 1):
    """Generate n number of zygotes."""
    sample = []
    for _ in range(0, n):
        sample.append(
            Gene(Allele(random_chars().send(None)), Allele(random_chars().send(None)))
        )
    yield sample


# --------------------------------------------------------------------------- #
async def async_population_generator(samples: int = 1):
    return population_generator(samples).__next__()


# --------------------------------------------------------------------------- #
async def async_chunked_population_generator(samples: int = 1):
    start = perf_counter()
    tasks = []
    # first we find the least common multiple of the number of samples
    lcm = least_common_divisor(samples)
    # get the chunk size based on the least common multiple and the
    # number of digits in the number of samples as the exponent
    # chunk_size = quantity of samples requested // (lcm ** length of digits in samples)
    chunk_size = samples // (lcm ** len(str(samples * lcm)))
    # then we create a container to hold the samples
    samples_container = []
    # print the info
    log.info(
        f"\nSamples: {samples}"
        f"\nLeast Common Multiple: {lcm}"
        f"\nChunk Size: {chunk_size}"
    )

    # lastly we iterate over the chunk size and append the chunked samples to the container
    while len(samples_container) < samples:
        task = asyncio.create_task(async_population_generator(chunk_size))
        tasks.append(task)
        res = await asyncio.gather(*tasks)
        samples_container.extend(res[0])
    end = perf_counter()
    log.info(
        f"\nTime Elapsed: {end - start:0.4f} seconds"
        f"\nNext Chunk Size: {len(samples_container)}"
    )
    return samples_container


# --------------------------------------------------------------------------- #
async def async_population_generator_handler(samples: int, **kwargs) -> List[Gene]:
    try:
        res = await async_chunked_population_generator(samples)
        return res[:samples]
    except StopIteration as e:
        log.info(f"Generator List error: {e}")
        pass


# --------------------------------------------------------------------------- #
def generate_population(n: int = 10):
    """Generate n number of zygotes."""
    res = asyncio.run(async_population_generator_handler(n))
    return res
