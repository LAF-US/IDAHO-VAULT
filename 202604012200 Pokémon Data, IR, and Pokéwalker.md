---
date created: Wednesday, April 1st 2026, 10:00:12 pm
date modified: Wednesday, April 1st 2026, 10:01:40 pm
related:
- '136'
- '236'
- '255'
- CRC
- NTR
- PCB
- RAM
- RESEARCH
- ROM
- algorithm
- numbers
authority: LOGAN
---
[♊](https://gemini.google.com/app)

RESEARCH: "Pokemon" as literal computer code ; HeartGold/SoulSilver infrared technology integration

## Gemini said

The concept of a "Pokémon" is often romanticized as a living creature, but in the realm of the Game Freak development environment, a Pokémon is a highly structured, **hexadecimal data block**.

In _HeartGold_ and _SoulSilver_ (HGSS), these data structures became more complex to accommodate the Nintendo DS’s hardware—specifically the unique infrared (IR) capabilities of the game cartridge itself.

### 1. The Pokémon as Literal Code

In Gen 4 (_HeartGold, SoulSilver, Diamond, Pearl, Platinum_), a Pokémon exists as a **136-byte or 236-byte structure** (the latter used when in your active party to store temporary battle stats).

The game doesn’t "see" a Pikachu; it sees a sequence of numbers partitioned into four 32-byte blocks (**A, B, C, and D**). To prevent simple save-editing, the game **shuffles** these blocks based on the Pokémon’s "Personality Value" (PV).

#### The Anatomy of a Data Block:

| Offset        | Data Type      | Function                                                                         |
| ------------- | -------------- | -------------------------------------------------------------------------------- |
| **0x00–0x03** | 32-bit Integer | **Personality Value (PV):** Determines gender, shininess, and nature.            |
| **0x08–0x0B** | 32-bit Integer | **Checksum:** A mathematical guard to ensure the data hasn't been corrupted.     |
| **0x0C–0x0D** | 16-bit Integer | **Species ID:** (e.g., `0x0019` for Pikachu).                                    |
| **0x1E**      | 8-bit Integer  | **Friendship/Happiness:** Stored as a value from 0–255.                          |
| **0x38–0x3B** | Bitfield       | **IVs & Flags:** Individual Values (0–31) and "Is Egg" or "Is Nicknamed" status. |

When you "transfer" a Pokémon, you aren't moving an object; you are performing a **memory copy** of these bytes from one device's RAM to another.

---

### 2. Infrared (IR) Technology Integration

The Nintendo DS and DS Lite did not have built-in infrared hardware. To facilitate the **Pokéwalker** and fast "IR Trading," Game Freak utilized a specialized cartridge type known as **NTR-031**.



#### The Hardware (The "Transparent" Cartridge)

If you hold an HGSS cartridge up to a strong light, you’ll notice it isn't solid grey; it's a **dark, translucent reddish-purple**. This material allows IR signals to pass through the casing to a dedicated transceiver chip embedded on the game's PCB.

#### The Pokéwalker Handshake

The Pokéwalker (the pedometer bundled with the games) acts as a thin client. It doesn't actually "run" the Pokémon game; it just displays data sent to it.

- **The Advertisement:** The Pokéwalker constantly sends a `0xFC` byte every few hundred milliseconds to say "I'm here."
    
- **The Transfer:** When you "Send a Pokémon," the DS encrypts the 136-byte Pokémon structure and transmits it via IR pulses.
    
- **The EEPROM Swap:** The Pokéwalker has its own small memory (EEPROM). The DS sends specific image data (sprites and text) to the Pokéwalker so the device knows how to "look" like your specific Pokémon without needing the entire game library stored on it.
    

#### Technical Synchronization

The IR communication uses a **checksum-validated packet system**. Each packet contains an 8-byte header:

1. **Command Byte:** (e.g., "Receive Pokémon" or "Sync Steps").
    
2. **Extra Data:** Variable.
    
3. **Checksum (2 bytes):** Uses a custom CRC algorithm to ensure no light interference corrupted the data.
    
4. **Session ID (4 bytes):** Prevents your DS from accidentally talking to a friend's Pokéwalker nearby.
    

---

### 3. Why it Matters

This IR integration was revolutionary for 2009 because it bypassed the clunky "Friend Code" and "Local Wireless" menus for certain tasks. By moving the communication to the **cartridge hardware** rather than the **console software**, Game Freak turned the game card itself into a specialized communication peripheral.

Are you looking into the technical structure of these files for a specific project, such as ROM hacking or data recovery?
