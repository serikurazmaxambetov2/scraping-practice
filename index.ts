import axios from "axios";
import { writeFile } from "fs/promises";

const PROXY_TYPES = ["http", "socks4", "socks5"] as const;
type ProxyType = (typeof PROXY_TYPES)[number];

async function scrapeProxy(proxyType: ProxyType) {
  const response = await axios.get<string>(
    `https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/${proxyType}.txt`
  );
  const proxies = response.data.trim().split("\n");
  return proxies.map((proxy) => `${proxyType}://${proxy}`);
}

async function scrape() {
  let allProxies: string[] = [];
  for (const proxyType of PROXY_TYPES) {
    const proxies = await scrapeProxy(proxyType);
    allProxies = allProxies.concat(proxies);
  }

  await writeFile("proxies.txt", allProxies.join("\n"));
}

scrape();
