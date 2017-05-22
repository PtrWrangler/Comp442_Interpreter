      entry
      addi   r14,r0,topaddr  % Set stack pointer

start addi   r1,r0,entx    % Ask for X
      sw     -8(r14),r1
      jl     r15,putstr

      addi   r1,r0,buf     % Get X
      sw     -8(r14),r1
      jl     r15,getstr
      jl     r15,strint    % Convert to integer
      sw     x(r0),r13     % Store X

      addi   r1,r0,enty    % Ask for Y
      sw     -8(r14),r1
      jl     r15,putstr

      addi   r1,r0,buf     % Get Y
      sw     -8(r14),r1
      jl     r15,getstr
      jl     r15,strint    % Convert to integer
      sw     y(r0),r13     % Store Y

      addi   r1,r0,0
      lw     r3,x(r0)      % r3 := X
      lw     r4,y(r0)      % r4 := Y