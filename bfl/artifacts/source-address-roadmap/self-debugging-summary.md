# Self-debugging addressed SourceWrite result

The bounded verification status is **passed**. Saturn first localized the
fresh-alphabet miss to the payload/consumer plane, relowered SourceWrite v2 through the frozen
recipient, then reassessed the paired surface and moved the next bounded update to the address
plane.

On the fresh-process 128-row heldout trial:

- address resolution: **113/128**;
- native: **5/128**;
- fixed address: **13/128**;
- learned address + relowered payload: **92/128**;
- oracle address + relowered payload: **105/128**;
- wrong source: **1/128**;
- random address: **11/128**;
- source zero: **5/128**, with candidate scores native-exact.

The previous fresh-alphabet oracle ceiling was 12/128. Recipient-local payload feedback raised it
to 105/128; address relowering then delivered 92/128 without an oracle at runtime. The fresh trial
contained no optimizer, donor model, donor trace, gold-label read, or oracle source-position read.

This is a development result, not a terminal claim. It is one synthetic task, checkpoint, length,
fresh alphabet, and compiler seed. Multi-token continuation and additional families remain open.
