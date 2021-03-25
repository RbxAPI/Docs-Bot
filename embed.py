from discord import Embed


def default_embed(author: str, **kwargs):
    emb = Embed(**kwargs)
    emb.set_author(name=author, icon_url="https://avatars1.githubusercontent.com/u/42101452?s=200&v=4")
    return emb


def footer_embed(message, author: str, icon_url: str = ''):
    emb = default_embed(author)
    emb.set_footer(text=f'\t\t\t\t\t\t\tTimestamp: {message.created_at}', icon_url=icon_url)
    return emb

