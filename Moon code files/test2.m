strint    addi  r13,r0,0      % R := 0 (result)
          addi  r4,r0,0       % S := 0 (sign)
          lw    r1,-8(r14)    % i := r1
          addi  r2,r0,0
strint1   lb    r2,0(r1)      % ch := B[i]
          cnei  r3,r2,32
          bnz   r3,strint2    % branch if ch != blank
          addi  r1,r1,1
          j     strint1
strint2   cnei  r3,r2,43
          bnz   r3,strint3    % branch if ch != "+"
          j     strint4
strint3   cnei  r3,r2,45
          bnz   r3,strint5    % branch if ch != "-"
          addi  r4,r4,1       % S := 1
strint4   addi  r1,r1,1       % i++
          lb    r2,0(r1)      % ch := B[i]
strint5   clti  r3,r2,48
          bnz   r3,strint6    % branch if ch < "0"
          cgti  r3,r2,57
          bnz   r3,strint6    % branch if ch > "9"
          subi  r2,r2,48      % ch -= "0"
          muli  r13,r13,10    % R *= 10
          add   r13,r13,r2    % R += ch
          j     strint4
strint6   ceqi  r3,r4,0
          bnz   r3,strint7    % branch if S = 0
          sub   r13,r0,r13    % R := -R
strint7   jr    r15