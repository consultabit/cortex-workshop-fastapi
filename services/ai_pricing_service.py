import constants as constants
import openai

class AIPricingService:
    GPT_4_TURBO = "gpt-4-1106-preview"
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo-1106"
    REQUEST = "request"
    RESPONSE = "response"

    def __init__(self):
        
        self.prices_per_1000_tokens = {
            self.GPT_4_TURBO: {
                self.REQUEST: 1,
                self.RESPONSE: 3
            },
            self.GPT_4: {
                self.REQUEST: 3,
                self.RESPONSE: 6
            },
            self.GPT_3_5_TURBO: {
                self.REQUEST: 0.1,
                self.RESPONSE: 0.2
            }
        }
        
        self.token_counts = {
            self.GPT_4_TURBO: {
                self.REQUEST: 0,
                self.RESPONSE: 0
            },
            self.GPT_4: {
                self.REQUEST: 0,
                self.RESPONSE: 0
            },
            self.GPT_3_5_TURBO: {
                self.REQUEST: 0,
                self.RESPONSE: 0
            }
        }
        
        self.total_costs = {
            self.GPT_4_TURBO: 0,
            self.GPT_4: 0,
            self.GPT_3_5_TURBO: 0
        }

        self.total_cost_in_usd_pennies = 0


    def amount_of_tokens_divided_by_1000(self, amount_of_tokens):
        return amount_of_tokens / 1000

    # Updates the individual costs for the GPT model and the total cost of all the models 
    def update_total_cost_for_model_and_request_or_response(self, gpt_model, amount_of_tokens, request_or_response):
        cost = self.amount_of_tokens_divided_by_1000(amount_of_tokens) * self.prices_per_1000_tokens[gpt_model][request_or_response]
        self.total_costs[gpt_model] += cost
        self.total_cost_in_usd_pennies += cost

    # Updates the token counts for the GPT model and the inputs and outputs
    def update_token_counts_for_model_and_request_or_response(self, gpt_model, amount_of_tokens, request_or_response):
        self.token_counts[gpt_model][request_or_response] += amount_of_tokens

    def calculate_token_costs_in_usd_pennies(self, messages_for_completion, completion, model):
        if model not in [self.GPT_4_TURBO, self.GPT_4, self.GPT_3_5_TURBO]:
            raise ValueError("Invalid model")
        
        # Get the token length of the request and response message
        tokens_from_request = self.openaiservice.tiktoken_count_amount_of_tokens(messages_for_completion[-1]["content"])
        tokens_from_response = self.openaiservice.tiktoken_count_amount_of_tokens(completion.choices[0].message.content)
        
        # Update the token counts and costs for the request and response by model
        self.update_token_counts_for_model_and_request_or_response(model, tokens_from_request, self.REQUEST)
        self.update_token_counts_for_model_and_request_or_response(model, tokens_from_response, self.RESPONSE)
        
        self.update_total_cost_for_model_and_request_or_response(model, tokens_from_request, self.REQUEST)
        self.update_total_cost_for_model_and_request_or_response(model, tokens_from_response, self.RESPONSE)

        # print(f"{self.GPT_4} COSTS: {self.total_costs[self.GPT_4]}")
        # print(f"{self.GPT_4_TURBO} COSTS: {self.total_costs[self.GPT_4_TURBO]}")
        # print(f"{self.GPT_3_5} COSTS: {self.total_costs[self.GPT_3_5]}")
        # print(f"TOTAL COST IN USD PENNIES: {self.total_cost_in_usd_pennies}")

        return self.total_cost_in_usd_pennies

    def get_total_cost_in_usd_pennies(self):
        return self.total_cost_in_usd_pennies