"""Random ironic messages assigned to each payer."""
import random

PAYMENT_MESSAGES = (
    "Cineva tocmai a cedat curiozității.",
    "Încă unul. Fără regrete.",
    "O minte curioasă a intrat în statistică.",
    "Altcineva a plătit 10 lei pe adevăr.",
    "Un nou număr de ordine. Acum.",
    "Cineva a ales să știe.",
    "Încă o persoană a apăsat butonul.",
    "Curiozitatea a câștigat din nou.",
    "Cineva tocmai a devenit parte din asta.",
    "Un om în plus. O sumă mai mare.",
    "Altcineva nu a putut rezista.",
    "Încă unul dintre noi.",
    "Cineva tocmai a intrat în club.",
    "10 lei mai puțin. Un număr mai mult.",
    "Altcineva a vrut să vadă.",
    "Cineva a decis că merită.",
    "Încă un curios și-a plătit biletul.",
    "Un om a plătit. Statistica a crescut.",
    "Cineva tocmai s-a numărat.",
    "Și totuși, a plătit.",
)


def random_payment_message():
    """Return a random ironic message to attach to a payer."""
    return random.choice(PAYMENT_MESSAGES)
