import serff_parser


parse = serff_parser.SERFFParser({"project": "test", "service":"test", "runtime":"python", "file": ""})
parse.fetch_source_files()