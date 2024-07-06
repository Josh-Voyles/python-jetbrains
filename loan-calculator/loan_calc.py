"""
Jet Brains Academy Project
Code by: Josh Voyles
Note: The course wanted all errors to print "Incorrect parameters."
"""
import argparse
import math
import textwrap


def positive_number(number):
    """
    Validate and return a positive number.

    :param number: The number to be validated.
    :return: The validated positive number.
    """
    val = float(number)
    if val <= 0:
        print("Incorrect parameters")
        exit()
    return val


def calculate_payment(loan_type, principal, interest_rate, months) -> str:
    """
    Calculate the payment for a loan based on the loan type, principal
    amount, interest rate, and number of months. Displays payment for each
    month.

    :param loan_type: The type of loan ('annuity' or 'diff'). :param
    principal: The principal amount of the loan. :param interest_rate: The
    interest rate for the loan. :param months: The number of months over
    which the loan will be repaid. :return: A string containing the
    calculated payment and overpayment details.

    """
    interest_rate = interest_rate / 100 / 12
    if loan_type == 'annuity':
        annuity = principal * (
                (interest_rate * (1 + interest_rate) ** months) /
                ((1 + interest_rate) ** months - 1))
        return textwrap.dedent(f"""
                Your annuity payment = {math.ceil(annuity)}!
                Overpayment = {round(math.ceil(annuity) * months - principal)}
                """)
    else:
        payments = []
        total_payment = 0
        for x in range(int(months)):
            payment = math.ceil(principal / months + interest_rate * (
                    principal - (principal * ((x + 1) - 1)) / months))
            string = f'Month {x + 1}: payment is {payment}\n'
            payments.append(string)
            total_payment += payment
        return textwrap.dedent(
            f"""{''.join(payments)}\nOverpayment = 
            {round(math.ceil(total_payment - principal))}""")


def calculate_principal(payment, interest_rate, months) -> str:
    """
    Calculate loan principal based on the given parameters.

    :param payment: The monthly payment amount.
    :param interest_rate: The annual interest rate.
    :param months: The number of months for the loan.
    :return: A formatted string containing the loan principal and overpayment.

    """
    interest_rate = interest_rate / 100 / 12
    principal = payment / ((interest_rate * (1 + interest_rate) ** months) / (
            (1 + interest_rate) ** months - 1))
    return textwrap.dedent(f'''
            Your loan principal = {math.floor(principal)}!
            Overpayment = {round(math.ceil(payment * months - principal))}''')


def calculate_months(payment, interest_rate, principal) -> str:
    """
    Calculate the number of months (or years) to repay a loan and the
    overpayment.

    :param payment: monthly payment amount
    :param interest_rate: annual interest rate
    :param principal: loan principal amount
    :return: string representation of the number of years, months,
    and overpayment
    """
    interest_rate = interest_rate / 100 / 12
    months = math.log((payment / (payment - interest_rate * principal)),
                      1 + interest_rate)
    months = math.ceil(months)
    overpayment = math.ceil(payment * months - principal)
    years = math.floor(months / 12)
    months = months - years * 12
    y_s = ''
    m_s = ''
    if years > 1:
        y_s = 's'
    if months > 1:
        m_s = 's'

    if years >= 1 and months >= 1:
        return ("It will take {} year{} and {} month{} to repay this "
                "loan!").format(
            years, y_s, months, m_s) + f"\nOverpayment = {overpayment}"
    elif months == 0:
        return "It will take {} year{} to repay this loan!".format(
            years, y_s) + f"\nOverpayment = {overpayment}"
    else:
        return "It will take {} month{} to repay this loan!".format(
            months, m_s) + f"\nOverpayment = {overpayment}"


def main() -> None:
    """
    The main function is used as an entry point for the Credit Calculator
    program. It retrieves command-line arguments using the argparse module
    and performs calculations based on those * arguments.

    :return: None
    """
    parser = argparse.ArgumentParser(description='Credit Calculator')
    parser.add_argument('--principal', type=positive_number,
                        help='Loan principal')
    parser.add_argument('--payment', type=positive_number, help='Loan payment')
    parser.add_argument('--periods', type=positive_number,
                        help='Number of periods(months)')
    parser.add_argument('--interest', type=positive_number,
                        help='Annual interest rate')
    parser.add_argument('--type', type=str, help='Type of loan')

    args = parser.parse_args()

    if not (args.type == 'diff' or args.type == 'annuity'):
        print('Incorrect parameters')
        exit()

    try:
        if args.payment is None:
            print(calculate_payment(args.type, args.principal, args.interest,
                                    args.periods))
        elif args.periods is None:
            print(
                calculate_months(args.payment, args.interest, args.principal))
        elif args.principal is None:
            print(
                calculate_principal(args.payment, args.interest, args.periods))
        else:
            print('Incorrect parameters')
    except TypeError:
        print('Incorrect parameters')


if __name__ == '__main__':
    main()
