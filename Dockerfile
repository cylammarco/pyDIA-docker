FROM raghurao/python-pyraf

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y wget

RUN wget https://repo.anaconda.com/archive/Anaconda2-2018.12-Linux-x86_64.sh
RUN chmod +x Anaconda2-2018.12-Linux-x86_64.sh && sh Anaconda2-2018.12-Linux-x86_64.sh -b

RUN /root/anaconda2/bin/conda install -y numpy scipy astropy matplotlib
RUN /root/anaconda2/bin/conda install -y -c pkgw/label/superseded pyraf
RUN /root/anaconda2/bin/conda install -y -c conda-forge scikit-learn
RUN /root/anaconda2/bin/conda install -y -c conda-forge scikit-image
RUN /root/anaconda2/bin/conda install -y -c anaconda make

RUN apt-get install -y git nano
RUN git clone https://github.com/MichaelDAlbrow/pyDIA
RUN cd pyDIA/Code && make CPU

ENV LD_LIBRARY_PATH "/root/anaconda2/lib:$LD_LIBRARY_PATH"
ENV PYTHONPATH "/root/anaconda2/lib/python2.7/site-packages:/pyDIA/Code:$PATH"

WORKDIR /iraf
