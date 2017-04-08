# pymon

PyMon is a lightweight, modular python based monitoring dashboard aimed at running on any device. It contains two parts, a monitoring daemon and a web-based reporting dashboard.

PyMon is still under heavy development. A few changes I still want to make:
 * remove the need of including bootstrap and the other libraries (resolve CORS conflicts)
 * Create modular pages
 * Provide a way to run this as a service, as opposed to via tmux


Installation instructions (linux)

```
git clone https://github.com/tr1plus/pymon pymon && cd pymon
apt-get install tmux libmysqlclient-dev
sudo pip install web.py schedule mysql-python psutil
./pymon start
```

Follow the onscreen instructions, and edit the config file where needed.


### Stuff used to make this:

 * [Bootstrap](http://getbootstrap.com/)
 * [Bootstrap color picker](https://itsjavi.com/bootstrap-colorpicker/)
 * [jQuery](https://jquery.com/)
 * [Deep Blue Admin Theme](http://www.prepbootstrap.com/bootstrap-theme/deepblue-admin)