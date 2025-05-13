<template>
    <v-container class="pt-16">
        <v-row>
            <v-col cols="'auto'" v-for="block in blocks" :key="block.link">
                <t-organ-card
                    :title="block.title"
                    :description="block.description"
                    :icon="block.icon"
                    :linkName="block.linkName"
                    :max-width="400"
                    :min-width="350"
                    :disabled="block.disabled"
                    class="h-100"
                >
                </t-organ-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { TOrganCard } from '@/components/widgets'

const blocks = [
    // {
    //     linkName: 'president',
    //     icon: 'president',
    //     description: `Законы РФ о поправке к Конституции РФ,
    //    федеральные конституционные законы, федеральные законы, указы Президента РФ,
    //    распоряжения Президента РФ`,
    //     title: 'Президент РФ',
    //     count: 8,
    //     disabled: false
    // },
    // {
    //     linkName: 'council_1',
    //     icon: 'council_1',
    //     description: `Постановления Совета Федерации, принятые по вопросам,
    //    отнесенным к ведению палаты частью 1 статьи 102 Конституции РФ`,
    //     title: 'Совет Федерации Федерального Собрания РФ',
    //     count: 1,
    //     disabled: false
    // },
    // {
    //     linkName: 'council_2',
    //     icon: 'council_2',
    //     description: `Постановления Государственной Думы, принятые по вопросам,
    //    отнесенным к ведению палаты частью 1 статьи 103 Конституции РФ`,
    //     title: 'Государственная Дума Федерального Собрания РФ',
    //     count: 1,
    //     disabled: false
    // },
    // {
    //     linkName: 'government',
    //     icon: 'government',
    //     description: 'Правовые акты Правительства РФ',
    //     title: 'Правительство РФ',
    //     count: 2,
    //     disabled: false
    // },
    // {
    //     linkName: 'federal_authorities',
    //     icon: 'federal_authorities',
    //     description:
    //         'Правовые акты федеральных органов исполнительной власти и федеральных государственных органов РФ',
    //     title: 'ФОИВ и ФГО РФ',
    //     count: 5,
    //     disabled: false
    // },
    // {
    //     linkName: 'court',
    //     icon: 'court',
    //     description:
    //         'Постановления Конституционного Суда РФ, определения Конституционного Суда РФ и иные решения Конституционного Суда РФ',
    //     title: 'Конституционный Суд РФ',
    //     count: 5,
    //     disabled: false
    // },
    // {
    //     linkName: 'subjects',
    //     icon: 'subjects',
    //     description: 'Законы и иные правовые акты субъектов РФ',
    //     title: 'Органы государственной власти субъектов РФ',
    //     count: 9,
    //     disabled: false
    // },
    // {
    //     linkName: 'international',
    //     icon: 'international',
    //     description:
    //         'Международные договоры, вступившие в силу для РФ, временно применяемые международные договоры РФ',
    //     title: 'Международные договоры РФ',
    //     count: 9,
    //     disabled: false
    // },
    // {
    //     linkName: 'un_securitycouncil',
    //     icon: 'un_securitycouncil',
    //     description: 'Резолюции Совета Безопасности Организации Объединённых Наций',
    //     title: 'Совет Безопасности ООН',
    //     count: 1,
    //     disabled: false
    // },
    {
        linkName: 'dashboard',
        icon: 'dashboard',
        description:
            'Информационная панель, обощающая информацию по количеству опубликованных нормативных правовых актатов РФ',
        title: 'Информационная панель',
        count: 1,
        disabled: false
    },
    {
        linkName: 'parser',
        icon: 'parser',
        description:
            'Информационная панель, обощающая информацию по количеству опубликованных нормативных правовых актатов РФ',
        title: 'Сбор данных',
        count: 1,
        disabled: false
    },
    {
        linkName: 'validator',
        icon: 'validator',
        description:
            'Информационная панель, обощающая информацию по количеству опубликованных нормативных правовых актатов РФ',
        title: 'Проверка документов',
        count: 1,
        disabled: false
    }
]
</script>
