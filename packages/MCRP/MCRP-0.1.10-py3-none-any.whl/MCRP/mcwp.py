"""
    MineCraft Watching Proxy
    ========================
"""

from MCRP import MCRewriteProxy, version
from .dgi import DeepGameInteractionMachine
from .util import CustomFormatter
from .iautil import addr_parser

import cubelib

from ruamel.yaml import YAML
import argparse
import logging
from importlib.machinery import SourceFileLoader
import traceback

BANNER = \
f"""
 __  __   ____  ____   ____       __        __ ____
|  \/  | / ___||  _ \ |  _ \  _   \ \      / /|  _ \\
| |\/| || |    | |_) || |_) |(_)   \ \ /\ / / | |_) |
| |  | || |___ |  _ < |  __/  _     \ V  V /  |  __/
|_|  |_| \____||_| \_\|_|    (_)     \_/\_/   |_| v{version}
"""

def main():

    print(BANNER[1:])
    parser = argparse.ArgumentParser(description="Minecraft Watching Proxy")
    parser.add_argument("-c", type=argparse.FileType("r", encoding="utf-8"), help="Path to the YAML config file", metavar="config.yaml")
    parser.add_argument("-v", action="store_true", help="If passed, enables verbose logging")
    parser.add_argument("-l", help="Proxy listen addr [localhost:25565] (enclose ipv6 like [::])", default="127.0.0.1:25565", metavar="addr")
    parser.add_argument("-u", help="Proxy upstream server addr [localhost:25575]", default="127.0.0.1:25575", metavar="addr")
    parser.add_argument("-d", help="Protocol decryption module", metavar="decmod")
    parser.add_argument("-ll", action="store_true", help="If passed, enables low level debug logging")
    parser.add_argument("--leave-debug-journals", action="store_true", help="If passed, leaves debug journals", dest="ldj")    
    parser.add_argument("--ext", help="Module with register() containing external handlers", metavar="handlers")
    parser.add_argument("-derf", action="store_true", help="Disable entities resolving and following")
    args = parser.parse_args()
    
    decryptor = SourceFileLoader("", f"{args.d}.py").load_module().MCWPDecryptor if args.d else None

    if args.c:
        yaml = YAML(typ="safe")
        conf = yaml.load(args.c)
    else:
        conf = {"mode": "blacklist"}

    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG if args.v else logging.INFO)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter('[%(asctime)s] [%(levelname)s] %(name)s:  %(message)s'))
    logger.addHandler(stdout_handler)

    # External handlers area
    if args.ext:
        try:
            external_handlers = SourceFileLoader("", f"{args.ext}.py").load_module().register
        except Exception as e:
            logger.error("Failed to load external handlers! There is no module with name given or it doesn't have register()")
            logger.error("\n" + traceback.format_exc())
            return

    limit = conf["loglimit"] if "loglimit" in conf else None
    if "mode" in conf:
        cbmode = conf["mode"]
        sbmode = conf["mode"]
    elif "ClientBoundMode" in conf and "ServerBoundMode" in conf:
        cbmode = conf["ClientBoundMode"]
        sbmode = conf["ServerBoundMode"]
        conf["mode"] = f"ClB: {cbmode} / SvB: {sbmode}"
    else:
        logger.error(f"Failed to read configuration! please declate 'mode' or 'ClientBoundMode' and 'ServerBoundMode'")
        exit()

    proxy = MCRewriteProxy(addr_parser(args.l, 25565), addr_parser(args.u, 25565),
        logging.DEBUG if args.ll else logging.INFO if args.v else logging.WARNING,
            decryptor=decryptor, leave_debug_journals=args.ldj)

    if args.ext:
        external_handlers(proxy)

    if args.derf:
        logger.info("Entities resolving and following are disabled!")

    ClientBoundFilterList = []
    ServerBoundFilterList = []

    @proxy.on(cubelib.proto.ServerBound.Handshaking.Handshake)
    def handler(packet):
        nonlocal ClientBoundFilterList, ServerBoundFilterList

        if packet.NextState != cubelib.NextState.Login:
            return cubelib.proto.ServerBound.Handshaking.Handshake(packet.ProtoVer, *addr_parser(args.u, 25565), packet.NextState)

        logger.debug(f'Selected proto version is: {packet.ProtoVer}, building filter...')
        proto = proxy.PROTOCOL

        def find_ap_by_path(proto, path):
            obj = proto
            attrs = path.split('.')
            if attrs[-1] == "NotImplementedPacket":
                return cubelib.p.NotImplementedPacket

            for attr in attrs:
                obj = getattr(obj, attr, None)
                if not obj:
                    logger.debug(f'\x1b[38;5;226mFailed to resolve filter packet {proxy.PROTOCOL.__name__}.{".".join(attrs)}')
                    break
            return obj
        
        ClientBoundFilterList = [find_ap_by_path(proto, "ClientBound.Play." + packet) for packet in conf["ClientBound"]] if "ClientBound" in conf else []
        ServerBoundFilterList = [find_ap_by_path(proto, "ServerBound.Play." + packet) for packet in conf["ServerBound"]] if "ServerBound" in conf else []
        ClientBoundFilterList = [i for i in ClientBoundFilterList if i is not None]
        ServerBoundFilterList = [i for i in ServerBoundFilterList if i is not None]

        logger.debug(f"Filtering mode: {conf['mode']}, filtered packets:")

        logger.debug(f"ClientBound [{len(ClientBoundFilterList)}]:")
        for fpacket in ClientBoundFilterList:
            logger.debug(f"    {fpacket}")

        logger.debug(f"ServerBound [{len(ServerBoundFilterList)}]:")
        for fpacket in ServerBoundFilterList:
            logger.debug(f"    {fpacket}")

        return cubelib.proto.ServerBound.Handshaking.Handshake(packet.ProtoVer, *addr_parser(args.u, 25565), packet.NextState)

    def log_clientbound(*args):
        logger.info(f'\u001b[96mClientBound   {" ".join([str(a) for a in args])}\u001b[0m')

    def log_serverbound(*args):
        logger.info(f'\u001b[95mServerBound   {" ".join([str(a) for a in args])}\u001b[0m')
    
    def log_rewrite(*args):
        logger.info(f'\x1b[38;2;186;220;88m{" ".join([str(a) for a in args])}\u001b[0m')

    def filter_(packet, mode, list_):
        if mode == "blacklist":
            if packet.__class__ in list_:
                return False
            return True

        elif mode == "whitelist":
            if packet.__class__ in list_:
                return True
            return False

    @proxy.ClientBound
    def handler(packet):
        packet = proxy.dgim(packet) if proxy.dgim else packet
        if filter_(packet, cbmode, ClientBoundFilterList):
            log_clientbound(packet) if not limit else log_clientbound(str(packet)[:limit])

    @proxy.ServerBound
    def handler(packet):
        packet = proxy.dgim(packet) if proxy.dgim else packet
        if filter_(packet, sbmode, ServerBoundFilterList):
            log_serverbound(packet) if not limit else log_serverbound(str(packet)[:limit])

    @proxy.Intersession
    def handler():        
        if not args.derf:
            proxy.dgim = DeepGameInteractionMachine(proxy)
        else:
            proxy.dgim = None

        print()
    
    @proxy.Rewrite
    def handler(source, replace):
        if replace != False:
            log_rewrite(source, "->", replace)

    def reload():
        """Re-load external handlers into the proxy instance"""
        proxy.purge_rel_handlers()
        if args.ext:
            try:
                external_handlers = SourceFileLoader("", f"{args.ext}.py").load_module().register
            except Exception as e:
                logger.error("Failed to load external handlers! There is no module with name given or it doesn't have register()")
                logger.error("\n" + traceback.format_exc())
        else:
            logger.error("You can't reload external handlers 'cause they are not being used!")
            return

        external_handlers(proxy)
        proxy.resolve_handlers()
    
    proxy.reload = reload

    proxy.join()

if __name__ == "__main__":
    main()
