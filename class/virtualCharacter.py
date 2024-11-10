class VirtualCharacter:
    def __init__ (id, name, role, look, characteristics, referenceImage, voice):
        self.id = id
        self.name = name
        self.role = role
        self.look = look
        self.characteristics = characteristics
        self.referenceImage = referenceImage    #image path
        self.voiceId = voice                    #voice object