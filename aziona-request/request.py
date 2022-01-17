# -*- coding: utf-8 -*-
"""Il modulo per la cancellazione di record DNS sul servizio route53 di AWS
"""
import sys
import json

from aziona.core import argparser, io
from aziona.core.conf import errors, session
import requests

def standard_args(parser):
    if not isinstance(parser, argparser.argparse.ArgumentParser):
        raise errors.ParamTypeError(param="parser", type="argparse.ArgumentParser")

    parser.add_argument(
        "--headers",
        default=None,
        type=str,
        help="Request headers",
    )
    parser.add_argument(
        "--data",
        default=None,
        type=str,
        help="Request post data",
    )
    parser.add_argument(
        "--method",
        default="GET",
        type=str,
        help="Request method",
    )
    parser.add_argument(
        "--url",
        default=None,
        type=str,
        help="Request endpoint url",
    )

    parser.add_argument("--account-id", default=None, type=str, help="AWS Account id")

    return parser


def argsinstance():
    parser = argparser.argparse.ArgumentParser()

    parser.add_argument("--action", required=True, type=str, help="Aws cli commands")

    standard_args(parser)
    argparser.standard_args(parser)
    argparser.action_args(parser)
    argparser.jq_args(parser)

    return parser


def load(args) -> None:
    """Esegue la logica del modulo.
    Args:
        args(dict,argparse.Namespace,optional): argomenti richiesti dal modulo
    Returns:
        None:
    """
    if isinstance(args, dict):
        args = argparser.namespace_from_dict(argsinstance()._actions, args)

    if not isinstance(args, argparser.argparse.Namespace):
        raise errors.ParamTypeError(param="args", type="argparse.Namespace")
    
    headers = {} if args.headers is None else json.loads(args.headers)
    data = {} if args.data is None else json.loads(args.data)
    response = requests.request(args.method.lower(), url=args.url, headers=headers, data=data)

    print(response.status_code, response.text)

    if args.session_save is not None:
        session.save(key=args.session_save, data={args.session_save: response.text})


def main() -> bool:
    try:
        load(args=argsinstance().parse_args())
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
