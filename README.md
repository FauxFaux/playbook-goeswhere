# playbook-goeswhere

This is a partial build for my linux machines. It sets them up how I like them,
I don't expect anyone else to like it, although you're welcome to try!

I use `ansible` in a weird way, because I don't like `ansible`'s data formats
or model: as much as possible is done in the `hosts` file, which is executable
python. This works surprisingly well. If you don't want the data inline, you
can put it in your own custom `yaml` format. It works out way better than
`ansible`'s tag model, I promise.

The aim here isn't to totally restore a machine from missing, backups and the
like are not handled. The aim is to get major software and config files in
place quickly, so I can start developing/building out on a new machine, if
needs be. Complex applications *are* stored here, because I don't install them
often enough to remember how to do it. This is the opposite of the way around
people normally automate things. Maybe they're right.

`ansible` divides stuff into `roles`. Which `roles` are on which machines is,
in my case, managed by the `hosts` file. These are the roles:

 * `base`: machine knows what it is
 * `owned`: I own this machine and will apply my preferences
 * `influx`: InfluxDB host
 * `prom`: Prometheus monitoring host

I manage my user account setup (e.g. i3wm config) in a different repository:
https://github.com/FauxFaux/rc
