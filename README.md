# ayanami_bel
 simple demotivator Bel telegram bot

### how to run bot
```bash
# open ~/.bashrc
# write to the end of the file export API_KEY="<TELEGRAM_TOKEN>"
# save & close file

# then apply by command source ~/.bashrc

git clone https://github.com/a1excoder/ayanami_bel
cd ayanami_bel/
sudo docker build --tag python-docker .
sudo docker run --restart=always -d -e API_KEY=$API_KEY python-docker
```

### ![@ptushkea](https://github.com/ptushkea) rewritten bot
