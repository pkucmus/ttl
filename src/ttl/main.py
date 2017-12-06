import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import click


TTL_FILE_PATH = os.path.expanduser(os.path.join('~', '.config', '.ttl-{}'))


@click.group()
def cli():
    pass


@cli.command()
@click.argument('who')
@click.argument('ticket')
def help(who, ticket):
    start_time = datetime.now()

    click.echo('Helping {} with ticket {}.'.format(who, ticket), color='white')

    try:
        while True:
            elapsed_time = datetime.now() - start_time
            click.echo(
                '\rTime elapsed: {} [ctrl] + [c] to stop'.format(elapsed_time),
                nl=False
            )
            time.sleep(0.1)
    except KeyboardInterrupt:
        description = click.prompt('\nDescription')
        save_entry(who, ticket, elapsed_time, description)


@cli.command()
@click.argument('date', default=datetime.now().strftime('%Y-%m-%d'))
def report(date):
    click.echo('Generating report for {}.'.format(date))
    entries = {}
    with ttl_file_open(date, read=True) as ttl_file:
        for line in ttl_file.readlines():
            who, ticket, elapsed_time, description = line.split(';;')
            hours, minutes, seconds = elapsed_time.split(':')
            seconds, microseconds = seconds.split('.')
            elapsed_timedelta = timedelta(
                hours=int(hours),
                minutes=int(minutes),
                seconds=int(seconds),
                microseconds=int(microseconds)
            )
            if ticket in entries:
                entries[ticket]['entries'].append(
                    (who, elapsed_timedelta, description.strip())
                )
                entries[ticket]['total_time'] += elapsed_timedelta
            else:
                entries[ticket] = {
                    'entries': [
                        (who, elapsed_timedelta, description.strip())
                    ],
                    'total_time': elapsed_timedelta
                }

    for ticket, data in entries.items():
        click.echo()
        click.echo('{}  https://jira/issue/{}'.format(ticket, ticket))
        click.echo('{} : {}'.format(
            strfdelta(
                data['total_time'],
                '{hours}:{minutes} ({hours}h {minutes}m)'
            ),
            ', '.join({desc[0] for desc in data['entries']})
        ))
        for desc in data['entries']:
            click.echo(desc[2])


def ttl_file_open(date=datetime.now().strftime('%Y-%m-%d'), read=False):
    file_path = TTL_FILE_PATH.format(date)
    my_file = Path(file_path)
    if read:
        file_mode = 'r'
    elif my_file.is_file():
        file_mode = 'a+'
    else:
        file_mode = 'w+'
    return open(file_path, file_mode)


def save_entry(who, ticket, elapsed_time, description):
    with ttl_file_open() as ttl_file:
        ttl_file.write(
            '{};;{};;{};;{}\n'.format(who, ticket, elapsed_time, description)
        )


def strfdelta(tdelta, fmt):
    data = {'days': tdelta.days}
    data['hours'], rem = divmod(tdelta.seconds, 3600)
    data['minutes'], data['seconds'] = divmod(rem, 60)
    return fmt.format(**data)
