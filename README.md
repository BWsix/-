# Shota URL Shortener

URL Shortener from the 2000s

### ec2 (ubuntu) quick start

```bash
# (spawn a tmux session by running `tmux`)
git clone --depth=1 https://github.com/BWsix/shota.git ~/shota && cd ~/shota
sudo HOST=`YOUR.DOMAIN.COM` ./aws/setup.sh
# (select OK)
HOST=`YOUR.DOMAIN.COM` uvicorn server.main:app
# (detach from the current tmux session by pressing: `C-b` `d`)
```
