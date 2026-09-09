# gautamx05 Profile Setup

1. Create a PUBLIC repository named exactly `gautamx05`.
2. Upload this package.
3. Run:
```bash
python scripts/radar.py --data assets/skills.json -o assets/radar
python scripts/radar.py --github gautamx05 -o assets/radar-langs --limit 7 --values --curve 0.4 --exclude "shell,makefile,dockerfile,batchfile,procfile"
python scripts/cards.py --user gautamx05 --out assets
python scripts/metrics.py --user gautamx05 --out assets
```
4. Push to `https://github.com/gautamx05/gautamx05.git`.
5. In Settings → Actions → General, enable Read and write permissions.
6. Run the three workflows once manually from Actions.
7. Edit `assets/skills.json` whenever you want to change your self-rated skills.

No photo, portfolio, Codeforces, or extra project is included. The only featured project is FinPilot-AI.
