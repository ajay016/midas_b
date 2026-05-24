/**
 * Tencent Chaos VM disassembler for kEc9hjFh5...js
 *
 * The VM uses a stack machine with ~67 opcodes.
 * Bytecode is encoded as base64 + RLE pairs and decoded by L().
 * The main program drives window.xMidas encryption.
 */

'use strict';

const fs = require('fs');

// ── 1. Load & extract the raw bytecode ──────────────────────────────────────

const src = fs.readFileSync(
  '/home/user/midas_b/kEc9hjFh5DQJbz_iPEWrfFxadMVk4PbLDS-5P8jE73pfdUuDwNGKNVZjdEztcHdofAVaHXo6zRGXgLwuvsK_afAEj6w_mKyiUmq-7AesIRU~.js',
  'utf8'
);

// R() – base64 decoder (matches the one in the source)
function R(C) {
  const E = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='.split('');
  let Q = String(C).replace(/[=]+$/, ''), I = 0, B = 0, g = '', L, A;
  while ((A = Q.charAt(B++))) {
    A = E.indexOf(A);
    if (~A && ((L = I % 4 ? 64 * L + A : A), I++ % 4)) {
      g += String.fromCharCode(255 & (L >> ((-2 * I) & 6)));
    }
  }
  return g;
}

// L() – RLE decoder (matches the one in the source)
function L(C) {
  const LStr = C[0], A = C[1].slice(), E = [], Q = R(LStr);
  let I = A.shift(), B = A.shift(), g = 0;
  function S() {
    while (g === I) { E.push(B); g++; I = A.shift(); B = A.shift(); }
  }
  for (let t = 0; t < Q.length; t++) {
    const m = Q[t].charCodeAt(0);
    S(); E.push(m); g++;
  }
  S();
  return E;
}

// ── 2. Pull the program data out of the source ────────────────────────────

// Find "var A = L([" and extract the two-element array
const progMatch = src.match(/var A = L\(\[\s*([\s\S]+?)\]\s*\)\s*;/);
if (!progMatch) { console.error('Could not find program data'); process.exit(1); }

// Eval the data in a safe sandbox (no DOM needed – just arrays + strings)
const dataStr = `([ ${progMatch[1]} ])`;
const progData = eval(dataStr);  // [ base64_string, [rle_pairs...] ]

const bytecode = L(progData);
console.log(`\n=== Bytecode length: ${bytecode.length} words ===\n`);

// ── 3. Opcode table (derived from E[] handler array in VM source) ─────────

const OPCODES = {
   0: 'KEYS',           // Object.keys(pop())
   1: 'DUP',            // push(TOS)
   2: 'STORE_DEREF',    // *L = *C  (pointer store via stack ref)
   3: 'SHL',            // TOS-1 <<= TOS
   4: 'EQ',             // TOS-1 == TOS
   5: 'INIT_ARRAY',     // ensure array at ref
   6: 'PUSH_STR',       // push ""
   7: 'EQQ',            // TOS-1 === TOS
   8: 'LOAD_IMM',       // push(next_word)   [1 operand]
   9: 'CALL_METHOD',    // call method; argcount=next_word
  10: 'STORE_REF0',     // *ref0 = TOS
  11: 'STORE_PROP',     // ref[0][ref[1]] = TOS
  // 12 is a hole
  13: 'ADD',            // TOS-1 += TOS
  14: 'APPEND_CHR',     // TOS += chr(next_word)  [1 operand]
  15: 'HAS_EXC',        // return !!exception
  16: 'DIV',            // TOS-1 /= TOS
  17: 'BOX',            // push([pop()])
  18: 'PUSH_TRUE',
  19: 'RETURN',
  20: 'JUMP',           // g = next_word  [1 operand]
  21: 'JUMP_IF_TRUE',   // if TOS: g = next_word  [1 operand]
  22: 'OR',             // TOS-1 |= TOS
  23: 'LOAD_DEREF',     // push(*pop())
  // 24 is a hole
  25: 'LOAD_PROP',      // push(C[0][C[1]])
  26: 'GTE',            // TOS-1 >= TOS
  27: 'NOT',            // push(!pop())
  28: 'PUSH_NULL',
  29: 'XOR',            // TOS-1 ^= TOS
  30: 'PUSH_UNDEF',
  // 31 is a hole
  32: 'AND',            // TOS-1 &= TOS
  33: 'MOD',            // TOS-1 %= TOS
  34: 'COPY_REF',       // *ref1 = *ref2
  35: 'GT',             // TOS-1 > TOS
  // 36 is a hole
  37: 'MAKE_VARREF',    // push([m[pop()][0], C])  (local var reference)
  38: 'MAKE_PROPREF',   // push([pop(), pop()].reverse())
  39: 'SWAP_N',         // swap TOS with TOS-N  [1 operand]
  40: 'NEW_FUNC',       // new ctor with stack args (no this)  [1 operand]
  41: 'CALL_FUNC',      // fn.apply(globalThis, args)  [1 operand]
  42: 'CLEAR_EXC',      // exception = null
  43: 'SET_TOS',        // TOS = next_word  [1 operand]
  44: 'SHR',            // TOS-1 >>>= TOS  (unsigned)
  45: 'POP',
  46: 'STORE_FROM_REF', // *ref2 = C[0][C[1]]
  // 47 is a hole
  48: 'MAKE_FUNC',      // create closure  [many operands]
  49: 'MUL',            // TOS-1 *= TOS
  50: 'COPY_PROP',      // L[0][L[1]] = C[0][C[1]]
  51: 'IN',             // TOS-1 in TOS
  52: 'PUSH_FALSE',
  53: 'POP_TRY',        // pop exception handler
  54: 'NEW_PROP',       // new obj.prop(...args)  [1 operand]
  // 55 is a hole
  56: 'LOAD_OUTER',     // push([outerScope[ref], C])
  57: 'MAKE_GLOBALREF', // push([globalThis, pop()])
  58: 'THROW',
  59: 'SETSTACK',       // m.length = next_word  [1 operand]
  // 60 is a hole
  61: 'ITER_NEXT',      // TOS.shift() with done flag
  // 62, 63 are holes
  64: 'ASR',            // TOS-1 >>= TOS  (signed)
  65: 'TRY_PUSH',       // push exception handler  [2 operands]
  66: 'SUB',            // TOS-1 -= TOS
  67: 'TYPEOF',         // push(typeof pop())
};

// Opcodes that consume extra immediate words from the stream
const OPERAND_COUNT = {
   8: 1,   // LOAD_IMM
   9: 1,   // CALL_METHOD (argcount)
  14: 1,   // APPEND_CHR
  20: 1,   // JUMP
  21: 1,   // JUMP_IF_TRUE
  39: 1,   // SWAP_N
  40: 1,   // NEW_FUNC
  41: 1,   // CALL_FUNC
  43: 1,   // SET_TOS
  54: 1,   // NEW_PROP
  59: 1,   // SETSTACK
  65: 2,   // TRY_PUSH (catch_addr, stack_depth)
  48: -1,  // MAKE_FUNC – variable; decoded separately
};

// ── 4. Disassemble ─────────────────────────────────────────────────────────

function disassemble(bc) {
  const lines = [];
  let i = 0;

  while (i < bc.length) {
    const addr = i;
    const op = bc[i++];

    if (op === 48) {
      // MAKE_FUNC: funcEntry(1), envCount(1), paramCount(1), env pairs, params
      const funcEntry  = bc[i++];
      const envCount   = bc[i++];
      const paramCount = bc[i++];
      const envPairs = [];
      for (let e = 0; e < envCount; e++) {
        envPairs.push(`slot[${bc[i++]}]=var[${bc[i++]}]`);
      }
      const params = [];
      for (let p = 0; p < paramCount; p++) params.push(bc[i++]);
      lines.push(
        `${String(addr).padStart(5)}  MAKE_FUNC  entry=@${funcEntry}  env=[${envPairs.join(', ')}]  params=[${params.join(', ')}]`
      );
      continue;
    }

    const name = OPCODES[op] || `UNK_${op}`;
    const nops = OPERAND_COUNT[op] || 0;
    const operands = [];
    for (let o = 0; o < nops; o++) operands.push(bc[i++]);

    const opsStr = operands.length
      ? '  ' + operands.map((v, idx) => {
          if ((op === 20 || op === 21 || op === 65) && idx === 0) return `@${v}`;
          if (op === 14) return `'${String.fromCharCode(v)}'`;
          return v;
        }).join(', ')
      : '';

    lines.push(`${String(addr).padStart(5)}  ${name.padEnd(16)}${opsStr}`);
  }
  return lines;
}

const lines = disassemble(bytecode);

// Write full disassembly to file
const out = lines.join('\n');
fs.writeFileSync('/home/user/midas_b/disasm_output.txt', out);
console.log(`Wrote ${lines.length} instructions to disasm_output.txt`);

// ── 5. Heuristic: find interesting patterns ────────────────────────────────

console.log('\n=== String literals (APPEND_CHR sequences) ===');
const strings = [];
let cur = null;
for (const ln of lines) {
  if (ln.includes('PUSH_STR')) { cur = { addr: ln.trim().split(/\s+/)[0], str: '' }; }
  else if (cur && ln.includes('APPEND_CHR')) {
    const m = ln.match(/'(.)'/);
    if (m) cur.str += m[1];
  } else if (cur && cur.str) {
    strings.push(cur);
    cur = null;
  } else { cur = null; }
}
strings.forEach(s => console.log(`  @${s.addr}: "${s.str}"`));

console.log('\n=== Jumps / branches ===');
lines.filter(l => l.includes('JUMP')).slice(0, 40).forEach(l => console.log(' ', l.trim()));

console.log('\n=== Calls (CALL_METHOD / CALL_FUNC) ===');
lines.filter(l => l.includes('CALL_METHOD') || l.includes('CALL_FUNC'))
  .slice(0, 40).forEach(l => console.log(' ', l.trim()));

console.log('\n=== XOR / AND / OR / MOD / MUL (crypto primitives) ===');
lines.filter(l => /\b(XOR|AND|OR|MOD|MUL|SHL|SHR|ASR)\b/.test(l))
  .slice(0, 60).forEach(l => console.log(' ', l.trim()));
