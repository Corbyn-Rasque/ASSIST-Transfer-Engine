from api.agreement.advisement    import Advisement,                         \
                                        AdditionalNToReach, NInAnyNAreas,   \
                                        NInNDifferentAreas, NFromUnits,     \
                                        NFollowing,         NToNFollowing
from api.agreement.sending       import Sending,                            \
                                        Articulation,       Template

# Only polymorphic api models are tested here; all others are tested in ./tests/fixtures

# Advisement
def test_advisement(advisement):
    examples = [
        advisement(AdditionalNToReach),
        advisement(NInAnyNAreas),
        advisement(NInNDifferentAreas),
        advisement(NFromUnits),
        advisement(NFollowing),
        advisement(NToNFollowing),
    ]

    for example in examples:
        parsed = Advisement.model_validate(example.dictionary).root
        assert parsed == example.model

# Sending Articulation
# def test_sending(sending):
#     examples = [
#         sending(Articulation),
#         sending(Template)
#     ]

#     for example in examples:
#         parsed = Sending.model_validate(example.dictionary).root
#         assert parsed == example.model
