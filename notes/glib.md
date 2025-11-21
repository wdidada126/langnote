# glib

https://gitlab.gnome.org/GNOME/glib/-/releases

wget https://gitlab.gnome.org/GNOME/glib/-/archive/2.72.3/glib-2.72.3.tar.gz


tar xf glib-*.tar.gz                    # unpack the sources
cd glib-*                               # change to the toplevel directory
meson _build                            # configure the build
ninja -C _build                         # build GLib

# Become root if necessary

ninja -C _build install                 # install GLib

