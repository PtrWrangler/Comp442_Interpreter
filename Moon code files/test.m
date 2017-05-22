% MOON simulator:

      entry
      addi   r14,r0,topaddr  % Set stack pointer

      lb r7,8(r8)
      putc r7
add   r2,r3,r4
      sw     tab(r1),r2
      align
      hlt

% ioj
tab   res    48            % Store results of operations
data    dw     1000, -35
