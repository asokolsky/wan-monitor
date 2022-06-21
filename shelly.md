# Shelly Commands

Sources:
https://shelly-api-docs.shelly.cloud/gen1/#http-dialect

## /shelly

```
alex@latitude7490:~/Projects/wan-monitor/ > curl -s http://192.168.10.190/shelly|jq
{
  "name": null,
  "id": "shellyplugus-083af2005bf0",
  "mac": "083AF2005BF0",
  "model": "SNPL-00116US",
  "gen": 2,
  "fw_id": "20220211-132652/plugusprod2_app-gcb4621f",
  "ver": "plugusprod2",
  "app": "PlugUS",
  "auth_en": false,
  "auth_domain": null
}
```
