import Head from 'next/head';

export default function Index() {
    return (
        <div>
            <Head>
                <title>RaizouRaider Next</title>
                <meta charSet='UTF-8' />
                <meta
                    name='viewport'
                    content='width=device-width, initial-scale=1.0'
                />
            </Head>
            <span style={{ fontSize: '32px' }}>
                RaizouRaider
                <span style={{ fontSize: '16px', color: 'lightgray' }}>
                    Next
                </span>
            </span>
        </div>
    );
}
