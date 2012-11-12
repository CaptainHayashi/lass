export VENV=$VIRTUAL_ENV
mkdir $VENV/packages && cd $VENV/packages
wget http://oligarchy.co.uk/xapian/1.2.7/xapian-core-1.2.7.tar.gz
wget http://oligarchy.co.uk/xapian/1.2.7/xapian-bindings-1.2.7.tar.gz
tar xzvf xapian-core-1.2.7.tar.gz
tar xzvf xapian-bindings-1.2.7.tar.gz
cd $VENV/packages/xapian-core-1.2.7
./configure --prefix=$VENV && make && make install
export LD_LIBRARY_PATH=$VENV/lib
cd $VENV/packages/xapian-bindings-1.2.7
./configure --prefix=$VENV --with-python --without-ruby --without-perl --without-php --without-tcl
make && make install
python -c "import xapian"
