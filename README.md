EveAsk
======

Q&amp;A Plateform for Eve Online Knowledge à la StackOverflow

## Getting Started
Clone the repository:

    git clone https://github.com/adrien-f/eveask.git
    
Install the dependencies (in a virtualenv):
    
    pip install -r requirements.txt
    
Setup the settings:

    cp eveask/settings_dist.py eveask/settings.py
    vim eveask/settings.py
    
Default env is 'dev', change it with EVEASK_ENV='prod'.

Run up the migrations and build the assets:

    python manage.py db upgrade
    python manage.py build_assets
    
Launch EveAsk:
    
    python run.py # Defaults on port 5000
    
    
## Contributing

Pull requests are most welcomed, but please come talk to us before at asylum@public.conference.talkinlocal.org (XMPP) to see what we're up to !

## License

The MIT License (MIT)

Copyright (c) 2014 @adrien-f

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


