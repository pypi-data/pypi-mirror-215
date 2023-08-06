import cubelib
from dataclasses import dataclass
import copy

@dataclass(repr=False)
class Entity:
    EType: None
    EntityID: int

    State: int = None
    Air: int = None
    NameTag: str = None
    ASNT: bool = None
    Silent: bool = None

    def apply(self, metadata: dict) -> dict:
        parsed = {}
        for metablock in metadata.copy():
            if metablock["index"] == 0:
                k = "State"
                v = int(metablock["value"])
                
            elif metablock["index"] == 1:
                k = "Air"
                v = int(metablock["value"])

            elif metablock["index"] == 2:
                k = "NameTag"
                v = str(metablock["value"])
            
            elif metablock["index"] == 3:
                k = "ASNT"
                v = bool(metablock["value"])
            
            elif metablock["index"] == 4:
                k = "Silent"
                v = bool(metablock["value"])
            else:
                continue

            setattr(self, k, v)
            parsed[k] = v
            metadata.remove(metablock)
        return parsed

    def __repr__(self):
        return f"<{self.EType}: {self.EntityID}>"
    
    def __str__(self):
        return self.__repr__()

@dataclass(repr=False)
class LivingEntityBase(Entity):
    Health: float = None
    PotionEffectColor: int = None
    IsPotionEffAmbient: bool = None
    ArrowsInEntity: int = None

    def apply(self, metadata: dict) -> dict:        
        parsed = super().apply(metadata)
        for metablock in metadata.copy():
            if metablock["index"] == 6:
                k = "Health"
                v = float(metablock["value"])

            elif metablock["index"] == 7:
                k = "PotionEffectColor"
                v = int(metablock["value"])

            elif metablock["index"] == 8:
                k = "IsPotionEffAmbient"
                v = bool(metablock["value"])

            elif metablock["index"] == 9:
                k = "ArrowsInEntity"
                v = int(metablock["value"])

            else:
                continue

            setattr(self, k, v)
            parsed[k] = v
            metadata.remove(metablock)
        return parsed

@dataclass(repr=False)
class LivingEntity(LivingEntityBase):
    AIEnabled: bool = None

    def apply(self, metadata: dict) -> dict:        
        parsed = super().apply(metadata)
        for metablock in metadata.copy():
            if metablock["index"] == 15:
                k = "AIEnabled"
                v = bool(metablock["value"])
            else:
                continue

            setattr(self, k, v)
            parsed[k] = v
            metadata.remove(metablock)
        return parsed    

@dataclass(repr=False)
class Ageable(LivingEntity):
    Age: int = None

    def apply(self, metadata: dict) -> dict:        
        parsed = super().apply(metadata)
        for metablock in metadata.copy():
            if metablock["index"] == 15:
                k = "Age"
                v = int(metablock["value"])
            else:
                continue

            setattr(self, k, v)
            parsed[k] = v
            metadata.remove(metablock)
        return parsed    
 
@dataclass(repr=False)
class ArmorStand(LivingEntityBase):
    Params: int = None
    HeadPos: tuple = None
    BodyPos: tuple = None
    LArmPos: tuple = None
    RArmPos: tuple = None
    LLegPos: tuple = None
    RLegPos: tuple = None

@dataclass(repr=False)
class Human(LivingEntityBase):
    SkinParts: int = None
    Reserved: int = None
    AbsHearts: float = None
    Score: int = None

    def apply(self, metadata: dict) -> dict:        
        parsed = super().apply(metadata)
        for metablock in metadata.copy():
            if metablock["index"] == 10:
                k = "SkinParts"
                v = int(metablock["value"])
            elif metablock["index"] == 16:
                k = "RSV"
                v = int(metablock["value"])
            elif metablock["index"] == 17:
                k = "AbsHearts"
                v = float(metablock["value"])            
            elif metablock["index"] == 18:
                k = "Score"
                v = int(metablock["value"])
            else:
                continue

            setattr(self, k, v)
            parsed[k] = v
            metadata.remove(metablock)
        return parsed  

class DeepGameInteractionMachine:

    def __init__(self, proxy) -> None:
        self.entities = {}
        self.proxy = proxy
    
    def __call__(self, packet: cubelib.p.Night) -> cubelib.p.Night:
        type_ = packet.__class__.__name__
        
        if type_ == "JoinGame" or type_ == "SpawnPlayer":
            e = Human('Player', packet.EntityID)            
            self.entities[packet.EntityID] = e

        elif type_ == "SpawnMob":
            e = LivingEntity(packet.Type, packet.EntityID)
            self.entities[packet.EntityID] = e

        elif type_ == "SpawnObject":
            if packet.Type == self.proxy.PROTOCOL.Object.ARMORSTAND:
                e = ArmorStand(packet.Type, packet.EntityID)            
            else:
                e = Entity(packet.Type, packet.EntityID)
            self.entities[packet.EntityID] = e

        packet = copy.copy(packet)
        if hasattr(packet, "EntityID"):
            if packet.EntityID in self.entities:
                packet.EntityID = self.entities[packet.EntityID]                

        if hasattr(packet, "Metadata"):          
            #print(packet.Metadata)  
            packet.Metadata = packet.EntityID.apply(packet.Metadata)
            #print(packet.Metadata)
        
        if hasattr(packet, "EntityIDs"):
            for eid in packet.EntityIDs:                
                if eid in self.entities:                    
                    packet.EntityIDs[packet.EntityIDs.index(eid)] = self.entities[eid]
                    if type_ == "DestroyEntities":
                        del self.entities[eid]

        return packet
    
