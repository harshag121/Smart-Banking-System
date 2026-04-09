const functions = require('firebase-functions');
const { WebhookClient } = require('dialogflow-fulfillment');
const { Card, Suggestion } = require('dialogflow-fulfillment');

// Mock database - In production, use Firestore or real banking API
const mockDatabase = {
    'user-123': {
        name: 'John Demo',
        accounts: {
            checking: {
                balance: 2547.83,
                accountNumber: '****4532',
                transactions: [
                    { date: '2026-04-08', desc: 'Grocery Store', amount: -87.43 },
                    { date: '2026-04-07', desc: 'Salary Deposit', amount: 3200.00 },
                    { date: '2026-04-06', desc: 'Electric Bill', amount: -124.50 },
                    { date: '2026-04-05', desc: 'Coffee Shop', amount: -5.60 },
                    { date: '2026-04-04', desc: 'Transfer from Savings', amount: 500.00 }
                ]
            },
            savings: {
                balance: 12750.00,
                accountNumber: '****7891',
                transactions: [
                    { date: '2026-04-01', desc: 'Interest Credit', amount: 12.50 },
                    { date: '2026-03-15', desc: 'Transfer to Checking', amount: -500.00 },
                    { date: '2026-03-01', desc: 'Deposit', amount: 1000.00 }
                ]
            }
        }
    }
};

// Session storage for pending transfers (in-memory, resets on function cold start)
const pendingTransfers = {};

exports.bankingWebhook = functions.https.onRequest((request, response) => {
    const agent = new WebhookClient({ request, response });

    // Get user ID from request (in demo, we use a static user)
    const userId = 'user-123';
    const user = mockDatabase[userId];

    function welcome(agent) {
        agent.add(`Welcome to Demo Bank! 🏦\n\nHello ${user.name}, I can help you with:\n• Check account balances\n• Transfer money between accounts\n• View recent transactions\n\nWhat would you like to do?`);
        agent.add(new Suggestion('Check Balance'));
        agent.add(new Suggestion('Transfer Money'));
        agent.add(new Suggestion('Transactions'));
    }

    function checkBalance(agent) {
        const accountType = agent.parameters['account-type'];

        if (accountType) {
            const account = user.accounts[accountType.toLowerCase()];
            if (account) {
                agent.add(`Your ${accountType} account (${account.accountNumber}) balance is:\n\n💰 **$${account.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}**`);
                agent.add(new Suggestion('Transfer Money'));
                agent.add(new Suggestion('View Transactions'));
            } else {
                agent.add(`I couldn't find your ${accountType} account. You have:\n• Checking: $${user.accounts.checking.balance}\n• Savings: $${user.accounts.savings.balance}`);
            }
        } else {
            // Show all balances
            agent.add(`Here are your account balances:\n\n🏦 **Checking** (${user.accounts.checking.accountNumber}): $${user.accounts.checking.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}\n💎 **Savings** (${user.accounts.savings.accountNumber}): $${user.accounts.savings.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}\n\nTotal: $${(user.accounts.checking.balance + user.accounts.savings.balance).toLocaleString('en-US', { minimumFractionDigits: 2 })}`);
            agent.add(new Suggestion('Transfer Money'));
            agent.add(new Suggestion('Transaction History'));
        }
    }

    function transferMoney(agent) {
        const amount = agent.parameters.amount;
        const fromAccount = agent.parameters['from-account']?.toLowerCase();
        const toAccount = agent.parameters['to-account']?.toLowerCase();
        const sessionId = request.body.session;

        // Validate accounts
        if (!user.accounts[fromAccount] || !user.accounts[toAccount]) {
            agent.add(`I couldn't find one of those accounts. You have:\n• Checking\n• Savings\n\nPlease specify both accounts.`);
            return;
        }

        if (fromAccount === toAccount) {
            agent.add(`You can't transfer money to the same account. Please choose different accounts.`);
            return;
        }

        // Extract numeric amount
        const transferAmount = amount.amount || parseFloat(amount);

        if (!transferAmount || transferAmount <= 0) {
            agent.add(`Please specify a valid amount to transfer.`);
            return;
        }

        // Check sufficient funds
        if (user.accounts[fromAccount].balance < transferAmount) {
            agent.add(`❌ Insufficient funds in your ${fromAccount} account.\nAvailable: $${user.accounts[fromAccount].balance}\nRequested: $${transferAmount}`);
            return;
        }

        // Store pending transfer
        pendingTransfers[sessionId] = {
            amount: transferAmount,
            from: fromAccount,
            to: toAccount,
            timestamp: new Date().toISOString()
        };

        agent.add(`Please confirm your transfer:\n\n💸 **$${transferAmount.toFixed(2)}**\nFrom: ${fromAccount.charAt(0).toUpperCase() + fromAccount.slice(1)}\nTo: ${toAccount.charAt(0).toUpperCase() + toAccount.slice(1)}\n\nDo you want to proceed?`);
        agent.add(new Suggestion('Yes, confirm'));
        agent.add(new Suggestion('No, cancel'));
    }

    function confirmTransfer(agent) {
        const sessionId = request.body.session;
        const transfer = pendingTransfers[sessionId];

        if (!transfer) {
            agent.add(`I don't see any pending transfer. Would you like to start a new transfer?`);
            agent.add(new Suggestion('Transfer Money'));
            return;
        }

        // Execute transfer (update mock database)
        user.accounts[transfer.from].balance -= transfer.amount;
        user.accounts[transfer.to].balance += transfer.amount;

        // Add transaction records
        const now = new Date().toISOString().split('T')[0];
        user.accounts[transfer.from].transactions.unshift({
            date: now,
            desc: `Transfer to ${transfer.to}`,
            amount: -transfer.amount
        });
        user.accounts[transfer.to].transactions.unshift({
            date: now,
            desc: `Transfer from ${transfer.from}`,
            amount: transfer.amount
        });

        // Clear pending
        delete pendingTransfers[sessionId];

        agent.add(`✅ **Transfer Successful!**\n\n$${transfer.amount.toFixed(2)} has been transferred from your ${transfer.from} to your ${transfer.to} account.\n\nNew Balances:\n• ${transfer.from}: $${user.accounts[transfer.from].balance.toFixed(2)}\n• ${transfer.to}: $${user.accounts[transfer.to].balance.toFixed(2)}`);
        agent.add(new Suggestion('Check Balance'));
        agent.add(new Suggestion('Another Transfer'));
    }

    function transactionHistory(agent) {
        const accountType = agent.parameters['account-type']?.toLowerCase() || 'checking';
        const account = user.accounts[accountType];

        if (!account) {
            agent.add(`Account not found. Showing checking account transactions:`);
            return transactionHistory(agent);
        }

        let response = `📊 **Recent ${accountType.charAt(0).toUpperCase() + accountType.slice(1)} Transactions:**\n\n`;

        account.transactions.slice(0, 5).forEach((tx, index) => {
            const emoji = tx.amount > 0 ? '💵' : '💸';
            const amountStr = tx.amount > 0 ? `+$${tx.amount.toFixed(2)}` : `-$${Math.abs(tx.amount).toFixed(2)}`;
            response += `${emoji} ${tx.date} - ${tx.desc}\n   ${amountStr}\n\n`;
        });

        response += `Current Balance: $${account.balance.toFixed(2)}`;

        agent.add(response);
        agent.add(new Suggestion('Check Savings'));
        agent.add(new Suggestion('Transfer Money'));
    }

    function fallback(agent) {
        agent.add(`I'm not sure I understand. You can say:\n• "Check my balance"\n• "Transfer $100 to savings"\n• "Show my transactions"\n• "Help"`);
        agent.add(new Suggestion('Help'));
    }

    // Intent map
    let intentMap = new Map();
    intentMap.set('Default Welcome Intent', welcome);
    intentMap.set('Check Balance', checkBalance);
    intentMap.set('Transfer Money', transferMoney);
    intentMap.set('Confirm Transfer - yes', confirmTransfer);
    intentMap.set('Transaction History', transactionHistory);
    intentMap.set('Default Fallback Intent', fallback);

    agent.handleRequest(intentMap);
});