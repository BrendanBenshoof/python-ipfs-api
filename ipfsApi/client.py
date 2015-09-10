"""
IPFS API Bindings for Python
"""
from . import http
from . import utils
from .commands import Command, \
                      ArgCommand, \
                      FileCommand
from .exceptions import InvalidCommand



class Client(object):

    __client__ = http.HTTPClient

    # BASIC COMMANDS
    def add(self,path,**flags):
        """

        """
        return self._add.prepare(self._client, **self._defaults)(path,*flags)

    def id(self):
        return self._id.prepare(self._client, **self._defaults)()


    def __init__(self,
                 host='127.0.0.1',
                 port=5001,
                 base='api/v0',
                 default_enc='json',
                 **defaults):

        self._client = self.__client__(host, port, base, default_enc)

        # default request keyword-args
        if defaults.has_key('opts'):
            defaults['opts'].update({'encoding': default_enc})
        else:
            defaults.update({'opts': {'encoding': default_enc}})

        self._defaults = defaults


        ############
        # COMMANDS #
        ############

        # BASIC COMMANDS
        self._add                = FileCommand('/add')
        self._cat                =  ArgCommand('/cat')
        self._ls                 =  ArgCommand('/ls')
        self._refs               =  ArgCommand('/refs')

        # DAT_A STRUCTURE COMMANDS
        self._block_stat         =  ArgCommand('/block/stat')
        self._block_get          =  ArgCommand('/block/get')
        self._block_put          = FileCommand('/block/put', accept_multiple=False)
        self._object_data        =  ArgCommand('/object/data')
        self._object_links       =  ArgCommand('/object/links')
        self._object_get         =  ArgCommand('/object/get')
        self._object_put         = FileCommand('/object/put')
        self._object_stat        =  ArgCommand('/object/stat')
        self._object_patch       =  ArgCommand('/object/patch')
        self._file_ls            =  ArgCommand('/file/ls')

        # ADV_ANCED COMMANDS
        self._resolve            =  ArgCommand('/resolve')
        self._name_publish       =  ArgCommand('/name/publish')
        self._name_resolve       =     Command('/name/resolve')
        self._dns                =  ArgCommand('/dns')
        self._pin_add            =  ArgCommand('/pin/add')
        self._pin_rm             =  ArgCommand('/pin/rm')
        self._pin_ls             =     Command('/pin/ls')
        self._repo_gc            =     Command('/repo/gc')

        # NET_WORK COMMANDS
        self._id                 =     Command('/id')
        self._bootstrap          =     Command('/bootstrap')
        self._swarm_peers        =     Command('/swarm/peers')
        self._swarm_addrs        =     Command('/swarm/addrs')
        self._swarm_connect      =  ArgCommand('/swarm/connect')
        self._swarm_disconnect   =  ArgCommand('/swarm/disconnect')
        self._swarm_filters_add  =  ArgCommand('/swarm/filters/add')
        self._swarm_filters_rm   =  ArgCommand('/swarm/filters/rm')
        self._dht_query          =  ArgCommand('/dht/query')
        self._dht_findprovs      =  ArgCommand('/dht/findprovs')
        self._dht_findpeer       =  ArgCommand('/dht/findpeer')
        self._dht_get            =  ArgCommand('/dht/get',
                                              decoder='json',
                                              post_hook=lambda r: r[u"Extra"])
        self.dht_put            =  ArgCommand('/dht/put', argc=2)
        self.ping               =  ArgCommand('/ping')

        # TOOL COMMANDS
        self.config             =  ArgCommand('/config')
        self.config_show        =     Command('/config/show')
        self.config_replace     =  ArgCommand('/config/replace')
        self.version            =     Command('/version')



    ###########
    # HELPERS #
    ###########

    def add_str(self, string, **kwargs):
        """Adds a Python string as a file to IPFS."""
        res = self.add(utils.make_string_buffer(string), **kwargs)
        try:
            return res['Hash']
        except:
            return res

    def add_json(self, json_obj, **kwargs):
        """Adds a json-serializable Python dict as a json file to IPFS."""
        res = self.add(utils.make_json_buffer(json_obj), **kwargs)
        try:
            return res['Hash']
        except:
            return res

    def get_json(self, multihash, **kwargs):
        """Loads a json object from IPFS."""
        return self.cat(multihash, decoder='json', **kwargs)

    def add_pyobj(self, py_obj, **kwargs):
        """Adds a picklable Python object as a file to IPFS."""
        res = self.add(utils.make_pyobj_buffer(py_obj), **kwargs)
        try:
            return res['Hash']
        except:
            return res

    def get_pyobj(self, multihash, **kwargs):
        """Loads a pickled Python object from IPFS."""
        return utils.parse_pyobj(self.cat(multihash, **kwargs))
