"""
    MineCraft Rewrite Proxy
    =======================
"""

import traceback
import logging
from importlib import import_module
from unittest.mock import MagicMock
from time import time
from Crypto.Cipher import AES
import datetime

import cubelib
import MCRP

from .tcproxy import tcproxy

from typing import Optional, List, Callable, Tuple, Union
from types import ModuleType

from copy import copy
import json

Relative = MagicMock()

class DebugJournal:

    def __init__(self, file_path: str):
        self.file = open(file_path, "wb")
    
    def append_clientbound(self, packet: bytes):
        self.add_record(type=0x01, data=packet)
    
    def append_serverbound(self, packet: bytes):
        self.add_record(type=0x02, data=packet)
    
    def set_enckey(self, key: bytes):
        self.add_record(type=0x03, data=key)

    def add_record(self, type: int, data: bytes):

        self.file.write(cubelib.types.VarInt.build(type))
        self.file.write(cubelib.types.VarInt.build(len(data)))
        self.file.write(data)
    
    def close(self):
        self.file.close()

class ProtocolDecryptor:
    """
        Protocol Decryptor Prototype
    """

    name: str
    version: str

    def __init__(self, logger):
        pass

    def EncryptionRequest(self, server_id: str, public_key: bytes, verify_token: str) -> Tuple[bytes, str, str]:
        """
        External Encryption Request handler for decryption setup purposes

        Args:
            server_id (str): EncryptionRequest.ServerID
            public_key (bytes): EncryptionRequest.PublicKey
            verify_token (bytes): EncryptionRequest.VerifyToken
        
        Returns:
            server_id (str): New server id
            public_key (bytes): New public key
            verify_token (bytes): New verify token
        """        
        pass
    
    def EncryptionResponse(self, shared_secret: bytes, verify_token: bytes) -> Tuple[bytes, bytes, bytes]:
        """
        External Encryption Response handler for decryption setup purposes

        Args:
            shared_secret (bytes): EncryptionResponse.SharedSecret
            verify_token (bytes): EncryptionResponse.VerifyToken
        
        Returns:
            shared_secret (bytes): Plain shared secret
            shared_secret (bytes): Encrypted shared secret
            verify_token (bytes): Encrypted verify token
        """          
        pass

class AESCipher:
    
    Encryptor: AES
    Decryptor: AES

    def __init__(self, secret: bytes):
        self.Encryptor = AES.new(secret, AES.MODE_CFB, iv=secret)
        self.Decryptor = AES.new(secret, AES.MODE_CFB, iv=secret)

class AESComplex:

    ClientCipher: AESCipher
    ServerCipher: AESCipher

    def __init__(self, secret):
        self.ClientCipher = AESCipher(secret)
        self.ServerCipher = AESCipher(secret)

class MCRewriteProxy(tcproxy):    

    ServerBoundBuff: List[bytes]
    ClientBoundBuff: List[bytes]

    PROTOCOL: ModuleType = cubelib.proto
    STATE: cubelib.state = cubelib.state.Handshaking
    COMPRESSION_THR: int = -1

    PASS_THROUGH: bool = False
    decryptor: Optional[ProtocolDecryptor] = None
    cipher: AESComplex

    HANDLERS: dict # {cubelib.proto.v47.ServerBound.ChatMessage: [False, <function handler at 0x00000...>]}
    REL_HANDLERS: dict

    ServerBoundHandler: Optional[Callable] = None
    ClientBoundHandler: Optional[Callable] = None
    IntersessionHandler: Optional[Callable] = None
    RewriteHandler: Optional[Callable] = None
    
    def __init__(self, listen_addr: tuple, upstream_addr: tuple,
        loglevel = logging.ERROR, decryptor: Optional[ProtocolDecryptor] = None,
            leave_debug_journals: bool = False):
        
        self.ServerBoundBuff = [b""] # it's a little trick to make immutable type (bytes)
        self.ClientBoundBuff = [b""] # mutable to pass reference to it
        self.HANDLERS = {}
        self.REL_HANDLERS = {}
        self.leave_debug_journals = leave_debug_journals
        self.crx = 0
        self.srx = 0

        self.logger = logging.getLogger("MCRP")
        self.logger.setLevel(loglevel)
        super().__init__(listen_addr, upstream_addr)
        self.logger.info(f"Running MCRP v{MCRP.version} (cubelib version {cubelib.version})")
        self.logger.info(f"Proxying config is: \u001b[97m{':'.join([str(a) for a in listen_addr])} \u001b[92m-> \u001b[97m{':'.join([str(a) for a in upstream_addr])}")
        self.logger.info(f"Using protocol decryptor: {decryptor.name}/{decryptor.version}") if decryptor else None
        self.logger.info(f"Debug journals enabled!") if leave_debug_journals else None
        if decryptor:
            crlogger = logging.getLogger("MCRP/CRYPTO")
            crlogger.setLevel(loglevel)
            self.decryptor = decryptor(crlogger)              
    
    def _waiting_for_client(self):
        
        self.IntersessionHandler() if self.IntersessionHandler else None
        self.logger.info(f"Waiting for client connection...")

    def _new_client(self):

        self.logger.info(f"New client, creating connection to the server")
            
    def _new_server(self):

        self.estab_time = time()
        self.logger.info(f"Connected to the server")
        self.logger.info("Reseting state to Handshaking")
        self.STATE = cubelib.state.Handshaking
        self.PROTOCOL = cubelib.proto
        self.COMPRESSION_THR = -1
        self.ServerBoundBuff = [b""]
        self.ClientBoundBuff = [b""]
        self.PASS_THROUGH = False        
        self.cipher = None
        if self.leave_debug_journals:
            dt = datetime.datetime.now()
            m = dt.strftime("%B")[:3]
            ts = dt.strftime(f"%d {m} %Y %H-%M-%S")
            self.logger.info(f"Starting debug journaling in file [{ts}.mcdj]")
            self.journal = DebugJournal(f"{ts}.mcdj")            

        # Remove relative handlers for old protocol
        for handler in dict(self.HANDLERS):
            if self.HANDLERS[handler][0] == True:
                del self.HANDLERS[handler]        
    
    def _client_lost(self):

        self.logger.info(f"Client disconnected\n" + self.stats())
    
    def _server_lost(self):

        if self.leave_debug_journals:
            self.journal.close()
        self.logger.info(f"Server disconnected")

    def _server_error(self, error):
        
        self.logger.error(f"Failed to connect to the server due to an error: {error}")
    
    def _from_client(self, data):

        return self._handle_bytes(data, self.ServerBoundBuff, cubelib.bound.Server)

    def _from_server(self, data):

        return self._handle_bytes(data, self.ClientBoundBuff, cubelib.bound.Client)

    def _client_error(self, error):
        
        self.logger.critical(f"Failed to bind socket to local addr due to an error: {error}")
        exit()

    def _handle_bytes(self, data, buff, bound):

        if bound is cubelib.bound.Server:
            self.crx += len(data)
        else:
            self.srx += len(data)
        
        if self.leave_debug_journals:
            (self.journal.append_clientbound if bound is cubelib.bound.Client else self.journal.append_serverbound)(data)

        was_encrypted = False
        if self.cipher:
            if bound is cubelib.bound.Server:
                data = self.cipher.ServerCipher.Decryptor.decrypt(data)
            elif bound is cubelib.bound.Client:
                data = self.cipher.ClientCipher.Decryptor.decrypt(data)
            was_encrypted = True

        if data[:3] == b"\xFE\x01\xFA" and self.STATE == cubelib.state.Handshaking:
            self.logger.warn("Client sent legacy MC|PingHost! Unsupported! Enabling pass-trough!")
            self.PASS_THROUGH = True

        if self.PASS_THROUGH:
            r = b""
            if buff[0]:
                r += buff[0]
                buff[0] = b""
            r += data
            return r

        try:
            packs = []
            buff[0] += data
            buff[0] = cubelib.readPacketsStream(buff[0], self.COMPRESSION_THR, bound, packs)            

            ret = b""
            for p in packs:
                if self.PASS_THROUGH:
                    ret += p.build(self.COMPRESSION_THR if p.compressed else -1)
                    continue # if the Handshake is sent in one buffer with LoginStart
                             # but proto is unsupported, we need to skip it right there
                try:
                    hr = self._handle_packet(p)
                    if isinstance(hr, bytes):
                        ret += hr

                    elif isinstance(hr, cubelib.p.Night):
                        ret += hr.build(self.COMPRESSION_THR if p.compressed else -1)

                    elif hr is False:
                        pass

                    else:
                        ret += p.build(self.COMPRESSION_THR if p.compressed else -1)
                        if hr is not None:
                            self.logger.warn(f'обработчик вернул неизвестный тип ({hr})')                    

                except Exception as e:
                    self.logger.warn(f"Exception in {bound.name}Bound Handler: {e}")
                    self.logger.warn("\n" + traceback.format_exc())
                    ret += p.build(self.COMPRESSION_THR if p.compressed else -1)
            
            if self.cipher and was_encrypted:
                return self.cipher.ServerCipher.Encryptor.encrypt(ret) if bound is cubelib.bound.Server else self.cipher.ClientCipher.Encryptor.encrypt(data)            
            return ret

        except Exception as e:
            self.logger.error(f"Exception in {bound.name}Bound: {e}")
            self.logger.error(traceback.format_exc())            

    def _handle_packet(self, pack):
        
        p = pack.resolve(self.STATE, self.PROTOCOL)
        t = p.__class__

        # Global bound handlers
        if pack.bound == cubelib.bound.Client:
            self.ClientBoundHandler(p) if self.ClientBoundHandler else None
        else:
            self.ServerBoundHandler(p) if self.ServerBoundHandler else None                

        # Handle handshake
        if t is cubelib.proto.ServerBound.Handshaking.Handshake:
            self._handle_handshake(p)
            # Call a handler if exists, prematurely to prevent state check if proto hasn't been loaded
            return self.call_handlers(p)

        if self.STATE is cubelib.state.Login:
            
            # Handle SetCompression
            if t is self.PROTOCOL.ClientBound.Login.SetCompression:
                self.logger.info(f"Point of switching-on compression with threshold {p.Threshold}")
                self.COMPRESSION_THR = p.Threshold

            # Handle LoginSuccess
            if t is self.PROTOCOL.ClientBound.Login.LoginSuccess:
                self.STATE = cubelib.state.Play
                self.logger.info(f"State changed to {self.STATE}")
            
            # Handle EncryptionRequest
            if t is self.PROTOCOL.ClientBound.Login.EncryptionRequest:
                if self.decryptor:
                    hr = self.decryptor.EncryptionRequest(p.ServerID, p.PublicKey, p.VerifyToken)
                    return self.PROTOCOL.ClientBound.Login.EncryptionRequest(*hr)
                return

            # Handle EncryptionResponse
            if t is self.PROTOCOL.ServerBound.Login.EncryptionResponse:
                if self.decryptor:
                    hr = self.decryptor.EncryptionResponse(p.SharedSecret, p.VerifyToken)
                    self.cipher = AESComplex(hr[0])
                    self.logger.info(f"Protocol encryption is set, but you provided a shared secret")
                    self.logger.info(f"Shared secret: {hr[0].hex()}")
                    if self.leave_debug_journals:
                        self.journal.set_enckey(hr[0])
                    return self.PROTOCOL.ServerBound.Login.EncryptionResponse(*hr[1:])
                self.logger.warn(f"Minecraft client sent EncryptionResponse! That mean full symmetric encryption enabling, so we can't proceed with protocol analyzing. Just proxying!")
                self.PASS_THROUGH = True
                return
            
            elif self.STATE is cubelib.state.Play:
                pass
        
        return self.call_handlers(p)

    def _handle_handshake(self, p):

        if p.NextState == cubelib.NextState.Status:
            self.STATE = cubelib.state.Status
            return
        
        self.STATE = cubelib.state.Login
        self.logger.info(f"State changed to {self.STATE}, trying to load protocol v{p.ProtoVer}")
        if p.ProtoVer in cubelib.supported_versions:        
            self.PROTOCOL = import_module(f"cubelib.proto.v{p.ProtoVer}")
        else:
            self.logger.warn(f"Failed to load protocol v{p.ProtoVer}, looks like it's unsupported! Enabling enabling pass-through")
            self.PASS_THROUGH = True
            return

        self.logger.info(f"Successfuly loaded protovol v{p.ProtoVer}" + (f", compiling {len(self.REL_HANDLERS)} handlers..." if self.REL_HANDLERS else ""))
        self.resolve_handlers()

    def resolve_handlers(self) -> None:
        """Resolve relative handlers into version specific"""

        for handler in self.REL_HANDLERS:
            attrs = handler._extract_mock_name().split('.')[1:]
            obj = self.PROTOCOL
            for attr in attrs:
                obj = getattr(obj, attr, None)
                if not obj:
                    self.logger.warn(f'Failed to resolve handler {self.PROTOCOL.__name__}.{".".join(attrs)}')
                    break
            if obj:
                self.logger.debug(f"Successfully resolved {handler} into {obj}")
                self.HANDLERS[obj] = [True, self.REL_HANDLERS[handler]]

    def on(self, type_):
        def no(fun):
            if isinstance(type_, MagicMock):
                if type_ in self.REL_HANDLERS:
                    self.REL_HANDLERS[type_].append(fun)
                else:
                    self.REL_HANDLERS[type_] = [fun]
            else:
                if type_ in self.HANDLERS:
                    self.HANDLERS[type_][1].append(fun)
                else:
                    self.HANDLERS[type_] = [False, [fun]]
            return fun
        return no
    
    def purge_rel_handlers(self):
        """Remove active relative handlers"""

        for handler in dict(self.HANDLERS):
            if self.HANDLERS[handler][0] == True:
                del self.HANDLERS[handler]

        self.REL_HANDLERS = {}
    
    def sendClient(self, p) -> None:
        """Send packet to the client"""
        self.Client.sendall(p.build(self.COMPRESSION_THR))
    
    def chatClient(self, content: Union[str, dict]) -> None:
        """Send chat message to the client"""
        if isinstance(content, str):
            content = {"text": content}
        elif not isinstance(content, dict):            
            raise RuntimeError("chatClient requires str or dict")

        apacket = self.PROTOCOL.ClientBound.Play.ChatMessage
        pos = apacket.Position.System
        packet = apacket(json.dumps(content), pos)

        self.sendClient(packet)

    def call_handlers(self, packet) -> Union[bytes, cubelib.p.Night, bool, None]:
        """Call all handlers assigned to the packet type"""
        src = copy(packet)
        t = packet.__class__
        if t in self.HANDLERS:
            handlers_list = self.HANDLERS[t][1]
            output = None
            for handler in handlers_list:
                hr = handler(packet)
                if hr is not None:
                    output = hr
            if output is not None and output != src:
                self.RewriteHandler(src, output) if self.RewriteHandler else None            
            return output

    def ClientBound(self, handler):
        self.ClientBoundHandler = handler
    
    def ServerBound(self, handler):
        self.ServerBoundHandler = handler
    
    def Intersession(self, handler):
        self.IntersessionHandler = handler
    
    def Rewrite(self, handler):
        self.RewriteHandler = handler

    def stats(self):
        output = f"Session time: {round(time() - self.estab_time, 2)}s\n"
        output += f"from Client RX - {self.crx / 1e+06}MB\n"
        output += f"from Server RX - {self.srx / 1e+06}MB\n"

        return output

    def join(self):
        
        self.logger.info(f'Registred direct handlers list[{len(self.HANDLERS)}]:')
        for name, handlers in self.HANDLERS.items():
            self.logger.info(f"[{len(handlers[1])}]    {name}")

        self.logger.info(f'Registred relative handlers list[{len(self.REL_HANDLERS)}]:')
        for name, handlers in self.REL_HANDLERS.items():
            self.logger.info(f"[{len(handlers)}]    {'.'.join(name._extract_mock_name().split('.')[1:])}")

        self.logger.debug('Entering mainloop')
        super().join()
        if hasattr(self.PROTOCOL.ClientBound.Play, "Disconnect") and not self.cipher and not self.PASS_THROUGH:
            chat_component = json.dumps({"text": "", "extra": [{"text":"proxy closed\n", "bold": True, "color": "aqua"}, {"text":self.stats(), "color": "green"}]})
            p = self.PROTOCOL.ClientBound.Play.Disconnect(chat_component).build(self.COMPRESSION_THR)
        self.Client.send(p)
        self.Server.close()
        self.logger.debug('Exiting')
