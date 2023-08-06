from jsonmathpy.parser.service_provider import ParserServicesProvider
from jsonmathpy.core.iterator import Iterator
from jsonmathpy.core.lexer import Lexer
from jsonmathpy.core.parser import Parser
from jsonmathpy.core.token import TokenProvider
from jsonmathpy.core.nodes import NodeProvider
from jsonmathpy.shared.interfaces.parser_service import IParserService
from jsonmathpy.shared.models.node_keys import ConfigurationModels

class ParserService(IParserService):
    """
     Implements interface IParserService:
    """
    def __init__(self, node_configuration: ConfigurationModels):
        self.node_configuration = node_configuration
        self.parser_serice = ParserServicesProvider(
                                                        lexer                   = Lexer, 
                                                        parser                  = Parser, 
                                                        token_provider          = TokenProvider,
                                                        node_provider           = NodeProvider,
                                                        iterator                = Iterator,
                                                        configuration_models    = self.node_configuration
                                                    )

    def parse_string(self, string: str):
        return self.parser_serice.parse_string_service(string)

    def tokenize_string(self, string: str):
        return self.parser_serice.tokenize_string_service(string)
