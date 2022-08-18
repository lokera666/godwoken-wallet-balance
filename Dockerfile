FROM python:3.9

WORKDIR /config
COPY ./gw_balance.py ./requirements.txt /config/
RUN pip3 install -r requirements.txt
ENV PORT=3000

CMD "python3" "gw_balance.py" "$godwoken_rpc" "$godwoken_wallet"
