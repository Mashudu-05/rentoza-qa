import requests, time

query = """
{
  continents {
    code
    name
  }
}
"""

endpoint = "https://countries.trevorblades.com/"
runs = 50
durations = []

for _ in range(runs):
    start = time.time()
    res = requests.post(endpoint, json={"query": query})
    durations.append(time.time() - start)

avg = sum(durations) / runs
print(f"Average response time over {runs} runs: {avg:.3f} seconds")