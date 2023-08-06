#! /usr/bin/env python3
# -*- coding: utf-8 -*-

def confirm(question, default_choice='yes'):
    """
    Adds available choices indicator at the end of 'question',
    and returns True for 'yes' and False for 'no'.
    If answer is empty, falls back to specified 'default_choice'.

    PARAMETERS:
    - question is mandatory, and must be convertible to str.
    - default_choice is optional and can be:
        | None: no preference given, user must enter yes or no
        | 'yes'
        | 'no'

    If no valid input is found, it loops until it founds a suitable answer.
    Exception handling is at the charge of the caller.
    """
    valid = {'yes':True, 'y':True, 'ye':True, 'no':False, 'n':False}
    default_choice = str(default_choice).lower()
    if default_choice == 'none':
        prompt = ' [y/n] '
    elif default_choice == 'yes':
        prompt = ' [Y/n] '
    elif default_choice == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError('invalid default answer: "%s"' % default_choice)

    while True:
        print(str(question) + prompt)
        choice = input().lower()
        if default_choice != 'none' and choice == '':
            return valid[default_choice]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
