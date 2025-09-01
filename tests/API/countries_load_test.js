import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 }, // ramp-up
    { duration: '1m', target: 50 },  // sustained load
    { duration: '30s', target: 0 },  // ramp-down
  ],
};

const query = `
{
  countries {
    code
    name
    continent {
      name
    }
  }
}
`;

export default function () {
  const res = http.post('https://countries.trevorblades.com/', JSON.stringify({ query }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}