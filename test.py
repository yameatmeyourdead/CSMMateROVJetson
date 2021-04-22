poll = ("<><><>".encode()).decode()

end = poll.rfind("<")
strt = poll.rfind(">",0, -1)
print(strt)
strt = strt + 1 if strt != -1 else strt
poll = poll[strt:end]
print(poll)