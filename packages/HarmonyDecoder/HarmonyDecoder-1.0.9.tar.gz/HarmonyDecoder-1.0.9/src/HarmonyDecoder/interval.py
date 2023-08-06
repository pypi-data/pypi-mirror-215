'''Module with operations on intervals.

Attributes
----------
UNISONO : str
'''

from HarmonyDecoder.note import *

UNISONO:str = "1"
DIMINISHED_SECOND:str = "2>>"
AUGMENTED_UNISONO:str = "1<"
MINOR_SECOND:str = "2>"
MAJOR_SECOND:str = "2"
DIMINISHED_THIRD:str = "3>>"
AUGMENTED_SECOND:str = "2<"
MINOR_THIRD:str = "3>"
MAJOR_THIRD:str = "3"
DIMINISHED_FOURTH:str = "4>"
PERFECT_FOURTH:str = "4"
DOUBLE_DIMINISHED_FIFTH:str = "5>>"
AUGMENTED_FOURTH:str = "4<"
DIMINISHED_FIFTH:str = "5>"
PERFECT_FIFTH:str = "5"
DIMINISHED_SIXTH:str = "6>>"
AUGMENTED_FIFTH:str = "5<"
MINOR_SIXTH:str = "6>"
MAJOR_SIXTH:str = "6"
DIMINISHED_SEVENTH:str = "7>"
AUGMENTED_SIXTH:str = "6<"
MINOR_SEVENTH:str = "7"
MAJOR_SEVENTH:str = "7<"
DIMINISHED_OCTAVE:str = "8>"
OCTAVE:str = "8"

interval_semitones : dict[str, int] = {
    UNISONO : 0,            DIMINISHED_SECOND : 0,
    AUGMENTED_UNISONO : 1,  MINOR_SECOND : 1,
    MAJOR_SECOND : 2,       DIMINISHED_THIRD : 2,
    AUGMENTED_SECOND : 3,   MINOR_THIRD : 3,
    MAJOR_THIRD : 4,        DIMINISHED_FOURTH : 4,
    PERFECT_FOURTH : 5,     DOUBLE_DIMINISHED_FIFTH : 5,
    AUGMENTED_FOURTH : 6,   DIMINISHED_FIFTH : 6,
    PERFECT_FIFTH : 7,      DIMINISHED_SIXTH : 7,
    AUGMENTED_FIFTH : 8,    MINOR_SIXTH : 8,
    MAJOR_SIXTH : 9,        DIMINISHED_SEVENTH : 9,
    AUGMENTED_SIXTH : 10,   MINOR_SEVENTH : 10,
    MAJOR_SEVENTH : 11,     DIMINISHED_OCTAVE : 11
}

def semitones_between(note1:note, note2:note) -> int:
    '''Function to calculate distance in semitones between two notes.

    Parameters
    ----------
    note1 : note
        Start note

    note2 : note
        End note

    Returns
    -------
    int
        Number of semitones between two notes. It does not give information about octave of notes - distance is always positive or equal.

    Raises
    ------
    TypeError
        If ``note1`` or ``note2`` is NoneType.
    
    Examples
    --------
    >>> from HarmonyDecoder.note import note
    >>> C4 = note('C', 4)
    >>> D4 = note('D', 4)
    >>> C3 = note('C', 3)
    >>> semitones_between(C4, D4)
    2
    >>> semitones between(D4, C4)
    2
    >>> semitones between(C4, C4)
    0
    >>> semitones_between(C3, C4)
    12
    '''

    if note1 is None or note2 is None:
        raise TypeError("2 note have to be given to calculate distance between them.")

    if note1 > note2:
        tmp:note = note2
        note2 = note1
        note1 = tmp

    name_index:int = 0
    semitones:int = 0
    octave:int = note1.octave

    names:list[str] = list(all_notes.keys())

    while note2.octave != octave or note2.name != names[name_index]:
        name_index += 1

        if name_index >= len(names):
            name_index = 0
            octave += 1

        if all_notes[names[name_index]] != all_notes[names[name_index - 1]]:
            semitones += 1            

        if note1.octave == octave and note1.name == names[name_index]:
            semitones = 0

    return semitones

def set_octave_to_closest(to_set:note, source:note) -> None:
    '''Sets given note to ba as close to the second note as possible, by changing it's octave.

    Parameters
    ----------
    to set : note
        Note to be changed

    source : note
        Source note, to which ``to_set`` note will be aligned.
    '''
    help_1:note = to_set.copy()
    help_1.octave = source.octave

    help_2:note = help_1.copy()
    help_2.octave += 1

    help_3:note = help_1.copy()
    help_3.octave -= 1

    diff_1:int = semitones_between(help_1, source)
    diff_2:int = semitones_between(help_2, source)
    diff_3:int = semitones_between(help_3, source)

    diff_to_octave:dict[int, int] = {
        diff_1 : help_1.octave,
        diff_2 : help_2.octave,
        diff_3 : help_3.octave
    }

    minimum:int = min([diff_1, diff_2, diff_3])

    to_set.octave = diff_to_octave[minimum]