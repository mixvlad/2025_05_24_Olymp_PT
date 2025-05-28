# Transaction Conflict Resolution

This project implements a solution for finding the longest sequence of non-conflicting transactions. The program reads transaction data and determines the maximum number of transactions that can be executed without conflicts.

## Problem Description

Given a set of transactions, each with read and write sets, the program finds the longest sequence of transactions that can be executed without conflicts. A conflict occurs when one transaction writes to a location that another transaction reads from.

## Usage

The program reads input in the following format:
- First line: `n m` where n is the number of transactions and m is the number of memory locations
- For each transaction:
  - First line: `r_i w_i` where r_i is the number of read locations and w_i is the number of write locations
  - Second line: list of read locations
  - Third line: list of write locations

The output consists of:
- First line: length of the longest non-conflicting sequence
- Second line: the sequence of transaction numbers (1-indexed)

# Олимпиадные задачи c Олимпиада по программированию от Positive Technologies 24 мая 2025

[Ссылка на контест](https://contest.yandex.ru/contest/78439)

